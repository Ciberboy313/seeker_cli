import os
import platform
import requests
import json
import re
import asyncio
import functools
import logging

# Get the logger instance
logger = logging.getLogger('seeker_cli')

def clean_json_string(s):
    # Rimuove blocchi markdown
    if "```" in s:
        match = re.search(r"```(?:json)?(.*?)```", s, re.DOTALL)
        if match:
            s = match.group(1)
    return s.strip()

from . import config

# --- Caricamento del Cookbook di Funzionalità ---
# Questo blocco è stato spostato qui da config.py per permettere il logging.
# In un'architettura più grande, andrebbe gestito con un sistema di configurazione robusto.
config.WINDOWS_HACKS_COOKBOOK = ""
try:
    with open(config.COOKBOOK_FILE, "r", encoding="utf-8") as f:
        config.WINDOWS_HACKS_COOKBOOK = f.read()
except FileNotFoundError:
    logger.warning(f"Attenzione: File '{config.COOKBOOK_FILE}' non trovato. Le funzionalità avanzate potrebbero essere limitate.")
except Exception as e:
    logger.error(f"Errore nel caricamento di '{config.COOKBOOK_FILE}': {e}")


async def call_ollama(messages, system_prompt_template, tool_list_string):
    # Recupera info sistema
    cwd = os.getcwd()
    username = os.getlogin()
    os_name = platform.system()

    # Formatta il prompt con il template dello specialista
    formatted_system_prompt = system_prompt_template.format(
        cwd=cwd,
        username=username,
        os_name=os_name,
        cookbook=config.WINDOWS_HACKS_COOKBOOK,
        tool_list=tool_list_string
    )

    # Assicuriamo che il primo messaggio sia sempre il System Prompt aggiornato
    system_msg = {"role": "system", "content": formatted_system_prompt}
    
    # Filtra eventuali system prompt vecchi dalla history per non confondere il modello
    user_history = [m for m in messages if m['role'] != 'system']
    final_messages = [system_msg] + user_history

    payload = {
        "model": config.MODEL_NAME,
        "messages": final_messages,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.1, # Bassa temperatura per precisione tecnica
            "num_ctx": 8192,
            "num_predict": config.MAX_OUTPUT_TOKENS
        }
    }
    
    try:
        # Usa run_in_executor per non bloccare l'event loop di asyncio
        loop = asyncio.get_running_loop()
        
        # functools.partial per passare argomenti a requests.post nel thread executor
        blocking_call = functools.partial(requests.post, config.OLLAMA_URL, json=payload)
        
        resp = await loop.run_in_executor(None, blocking_call) # None usa l'executor di default (ThreadPoolExecutor)
        
        resp.raise_for_status()
        cleaned_content = clean_json_string(resp.json()['message']['content'])
        return cleaned_content
    except Exception as e:
        logger.error(f"Errore critico connessione Ollama: {e}")
        return json.dumps({
            "thought": "Errore di connessione",
            "action": "chat", 
            "args": {"message": f"Errore critico connessione Ollama: {e}"}
        })