import json
import logging
import re

import requests

from . import config
from .llm import clean_json_string


logger = logging.getLogger("seeker_cli")

VALID_CATEGORIES = {
    "programming_question",
    "system_command",
    "general_chat",
}


def _match_any(patterns, text):
    return any(re.search(pattern, text) for pattern in patterns)


def _heuristic_route(user_input):
    text = user_input.strip().lower()
    if not text:
        return "general_chat"

    if text.startswith("/"):
        return "system_command"

    system_patterns = [
        r"\b(apri|lancia|avvia|installa|disinstalla|esegui)\b",
        r"\b(open|launch|lounch|start|run|execute|install|uninstall)\b",
        r"\b(cerca|trova|ricerca|dove)\b",
        r"\b(search|find|locate|where)\b",
        r"\b(manual|manuals|handbook)\b",
        r"\b(copia|sposta|rinomina|elimina|cancella)\b",
        r"\b(copy|move|rename|delete|remove)\b",
        r"\b(file|cartell|directory|percorso|path)\b",
        r"\b(documents|documenti|desktop)\b",
        r"\b(mostr(a|ami)|lista|elenca)\b.*\b(file|cartell|directory)\b",
        r"\b(list|show)\b.*\b(files|folders|directories)\b",
        r"\b(theme|dark|light)\b",
        r"\b(tema|scuro|chiaro)\b",
        r"\bwindows\b.*\b(theme|tema|dark|light|scuro|chiaro)\b",
        r"\bchange\b.*\b(theme|dark|light)\b",
        r"\b(cambia|imposta)\b.*\b(tema|scuro|chiaro)\b",
        r"\b(cmd|powershell|terminal|shell)\b",
    ]

    programming_patterns = [
        r"\bpython\b",
        r"\bjavascript\b",
        r"\btypescript\b",
        r"\bjava\b",
        r"\bc\+\+\b",
        r"\bc#\b",
        r"\brust\b",
        r"\bgolang\b",
        r"\bsql\b",
        r"\bregex\b",
        r"\bapi\b",
        r"\bhttp\b",
        r"\btraceback\b",
        r"\bstack\s*trace\b",
        r"\bexception\b",
        r"\berror\b",
        r"\bbug\b",
        r"\bfunzione\b",
        r"\bclasse\b",
        r"\bmodulo\b",
        r"\bimport\b",
        r"\bdef\b",
        r"\bpackage\b",
        r"\bpip\b",
        r"\bnpm\b",
        r"\bcome\s+si\s+fa\b",
        r"\bin\s+(python|javascript|js|java)\b",
    ]

    if _match_any(system_patterns, text):
        return "system_command"
    if _match_any(programming_patterns, text):
        return "programming_question"

    return None


def _parse_router_output(raw_response):
    cleaned = clean_json_string(raw_response)
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass
    return {"category": cleaned}


def _normalize_category(value):
    if value is None:
        return ""
    return str(value).strip().lower().replace("`", "").replace('"', "")


def classify_request(user_input):
    heuristic_category = _heuristic_route(user_input)
    if heuristic_category:
        logger.debug("Router heuristic matched: %s", heuristic_category)
        return heuristic_category

    prompt = config.ROUTER_PROMPT_TEMPLATE.format(user_input=user_input)
    url = config.OLLAMA_URL.replace("/chat", "/generate")
    payload = {
        "model": config.ROUTER_MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.0},
    }

    try:
        response = requests.post(url, json=payload, timeout=config.ROUTER_TIMEOUT)
        response.raise_for_status()
        raw_output = response.json().get("response", "")
        data = _parse_router_output(raw_output)

        category = _normalize_category(data.get("category"))
        confidence = data.get("confidence", None)
        if confidence is not None:
            try:
                confidence = float(confidence)
            except (TypeError, ValueError):
                confidence = None

        if category in VALID_CATEGORIES:
            if confidence is not None and confidence < config.ROUTER_CONFIDENCE_THRESHOLD:
                logger.warning(
                    "Router confidence too low (%s). Falling back to general_chat.",
                    confidence,
                )
                return "general_chat"
            return category

        logger.warning(
            "Router output unexpected category: '%s'. Falling back to general_chat.",
            category,
        )
    except Exception as exc:
        logger.error("Errore chiamata al Router: %s", exc)

    return "general_chat"
