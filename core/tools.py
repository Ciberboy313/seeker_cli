import os
import subprocess
import difflib
import re
import requests
import logging
import string
from colorama import Fore, Style
from googlesearch import search
from .security import ask_permission
import shutil
import winreg
from . import config # Import config to get custom paths

logger = logging.getLogger('seeker_cli')

ITALIAN_STOPWORDS = {
    'a', 'ad', 'al', 'alla', 'allo', 'anche', 'ancora', 'che', 'chi', 'ci', 'cioè', 'ciò', 'come', 'con', 'contro',
    'da', 'dal', 'dalla', 'dallo', 'dei', 'del', 'della', 'dello', 'dentro', 'di', 'doppo', 'e', 'ecco', 'egli',
    'ella', 'entrambi', 'entrambe', 'essi', 'esse', 'fa', 'fai', 'fanno', 'fare', 'ha', 'hai', 'hanno',
    'ho', 'i', 'il', 'in', 'indietro', 'invece', 'io', 'la', 'le', 'lei', 'lo', 'loro', 'lui', 'ma', 'me', 'medesimo',
    'medesima', 'mentre', 'mio', 'mia', 'miei', 'mie', 'modo', 'molto', 'molti', 'molte', 'ne', 'negli', 'nei',
    'nel', 'nella', 'nelle', 'nello', 'no', 'non', 'nostro', 'nostra', 'nostri', 'nostre', 'o', 'ogni', 'oltre',
    'onde', 'ora', 'oppure', 'per', 'perchè', 'perciò', 'perfino', 'persino', 'più', 'pochi', 'poche', 'poi',
    'proprio', 'quale', 'quali', 'quanto', 'quanti', 'quanta', 'quante', 'quel', 'quello', 'quella', 'quelli',
    'quelle', 'questo', 'questa', 'questi', 'queste', 'qui', 'quindi', 'restando', 'se', 'sempre', 'senza',
    'si', 'siamo', 'siete', 'sono', 'sopra', 'sotto', 'sta', 'stai', 'stando', 'stanno', 'starai', 'sarà',
    'stato', 'stata', 'stati', 'state', 'stessa', 'stesse', 'stesso', 'stessi', 'su', 'suo', 'sua', 'suoi',
    'sue', 'tale', 'tali', 'tanto', 'tanti', 'tanta', 'tante', 'ti', 'tra', 'tu', 'tua', 'tuo', 'tuoi', 'tue',
    'tuttavia', 'tutto', 'tutta', 'tutti', 'tutte', 'un', 'una', 'uno', 'verso', 'voi', 'vostri', 'vostre',
    'vostro', 'vostra', 'è'
}

def _find_executable(executable_name):
    logger.debug(f"Searching for executable: {executable_name}")

    # 1. Check system PATH
    path = shutil.which(executable_name)
    if path and os.path.exists(path):
        logger.debug(f"Found in PATH: {path}")
        return path

    # 2. Check Registry (App Paths)
    try:
        for hkey in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
            with winreg.OpenKey(hkey, f"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\{executable_name}") as key:
                app_path, _ = winreg.QueryValueEx(key, "")
                if os.path.exists(app_path):
                    logger.debug(f"Found in App Paths registry: {app_path}")
                    return app_path
    except Exception:
        pass

    # 3. Enhanced Brute-force search in common and custom locations
    logger.debug("Executable not in PATH or App Paths. Starting enhanced brute-force search...")
    
    # Get all drives
    drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
    
    search_dirs = []
    # Add common folders for all drives
    for drive in drives:
        search_dirs.append(os.path.join(drive, "Program Files"))
        search_dirs.append(os.path.join(drive, "Program Files (x86)"))

    # Add user-specific folders
    search_dirs.append(os.path.join(os.path.expanduser('~'), 'AppData', 'Local'))
    search_dirs.append(os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming'))
    search_dirs.append(os.path.join(os.path.expanduser('~'), 'Desktop'))
    
    # Add custom paths from config
    if hasattr(config, 'CUSTOM_PROGRAM_PATHS'):
        search_dirs.extend(config.CUSTOM_PROGRAM_PATHS)

    for start_dir in set(search_dirs): # Use set to avoid duplicate searches
        if not os.path.isdir(start_dir):
            continue
        logger.debug(f"Searching in {start_dir}...")
        for root, dirs, files in os.walk(start_dir, topdown=True):
            # Prune search in common deep/irrelevant/permission-denied folders
            dirs[:] = [d for d in dirs if d.lower() not in [
                'node_modules', 'temp', 'cache', 'windowsapps', '$recycle.bin', 'system volume information'
            ]]
            
            if executable_name.lower() in (f.lower() for f in files):
                path = os.path.join(root, executable_name)
                logger.debug(f"Found via brute-force search: {path}")
                return path

    logger.warning(f"Executable '{executable_name}' not found after all search methods.")
    return None


def _get_everything_es_path():
    env_path = getattr(config, "EVERYTHING_ES_PATH", None)
    if env_path and os.path.exists(env_path):
        return env_path
    legacy_path = getattr(config, "EVERYTHING_CLI_PATH", None)
    if legacy_path and os.path.exists(legacy_path):
        return legacy_path
    default_path = r"C:\Program Files\Everything\es.exe"
    if os.path.exists(default_path):
        return default_path
    return None


def _get_everything_gui_path():
    env_path = getattr(config, "EVERYTHING_GUI_PATH", None)
    if env_path and os.path.exists(env_path):
        return env_path
    default_path = r"C:\Program Files\Everything\Everything.exe"
    if os.path.exists(default_path):
        return default_path
    return None


def _resolve_search_locations(location):
    candidates = []
    userprofile = os.environ.get("USERPROFILE") or os.path.expanduser("~")
    if userprofile:
        candidates.extend(
            [
                os.path.join(userprofile, "Documents"),
                os.path.join(userprofile, "Desktop"),
                os.path.join(userprofile, "Downloads"),
            ]
        )

    for key in ["OneDrive", "OneDriveConsumer", "OneDriveCommercial"]:
        base = os.environ.get(key)
        if base:
            candidates.extend(
                [
                    os.path.join(base, "Documents"),
                    os.path.join(base, "Desktop"),
                    os.path.join(base, "Downloads"),
                ]
            )

    existing = [p for p in candidates if p and os.path.isdir(p)]
    if not location:
        return existing

    location_lower = location.lower()
    if "documents" in location_lower or "documenti" in location_lower:
        return [p for p in existing if p.lower().endswith("documents")]
    if "desktop" in location_lower:
        return [p for p in existing if p.lower().endswith("desktop")]
    if "downloads" in location_lower or "download" in location_lower:
        return [p for p in existing if p.lower().endswith("downloads")]
    return existing


def _build_everything_variants(query, expand_variants=False):
    raw = query.strip()
    raw_lower = raw.lower()

    variants = [raw]
    if expand_variants and ("d&d" in raw_lower or "dnd" in raw_lower or "d and d" in raw_lower):
        variants = [
            "d&d",
            "dnd",
            "d and d",
            "dungeons and dragons",
            "players handbook",
            "phb",
        ]

    return [item for item in variants if item]


def _build_everything_query(query, expand_variants=False):
    raw = query.strip()
    variants = _build_everything_variants(raw, expand_variants=expand_variants)
    cleaned = []

    for item in variants:
        if " " in item:
            cleaned.append(f'"{item}"')
        else:
            cleaned.append(item)

    if not cleaned:
        return raw

    return " | ".join(cleaned)


def _build_everything_regex(query, expand_variants=False):
    variants = _build_everything_variants(query, expand_variants=expand_variants)
    if not variants:
        return ""
    escaped = [re.escape(item) for item in variants]
    return "|".join(escaped)

def _open_path(path):
    if ask_permission("aprire file o eseguire programma", path, is_dangerous=True):
        try:
            os.startfile(path)
            return f"'{os.path.basename(path)}' avviato con successo."
        except Exception as e:
            logger.error(f"ERRORE: Impossibile avviare '{path}': {e}")
            return f"ERRORE: Impossibile avviare '{path}': {e}"
    return "Utente ha negato l azione."

def tool_launch_program(program_name):
    path = _find_executable(program_name)
    if path:
        return _open_path(path)
    return f"ERRORE: Programma '{program_name}' non trovato. Impossibile avviare."


def tool_open_path(path):
    if not path:
        return "ERRORE: Percorso non valido."
    if os.path.exists(path):
        return _open_path(path)
    return f"ERRORE: File o cartella non trovata: '{path}'"


def _normalize_program_name(program_name):
    if not program_name:
        return None
    name = program_name.strip().lower()
    if name in {"blocco note", "blocconote", "notepad"}:
        return "notepad.exe"
    if not name.endswith(".exe") and " " not in name:
        return f"{program_name}.exe"
    return program_name


def tool_open_file(file_name, location=None, program_name=None):
    if not file_name:
        return "ERRORE: Nome file non valido."

    candidates = _resolve_search_locations(location)
    candidates.append(os.getcwd())

    normalized_program = _normalize_program_name(program_name)

    for base in candidates:
        candidate_path = os.path.join(base, file_name)
        if os.path.exists(candidate_path):
            if normalized_program:
                executable = _find_executable(normalized_program)
                if not executable:
                    return f"ERRORE: Programma '{program_name}' non trovato."
                return tool_execute(f'"{executable}" "{candidate_path}"')
            return _open_path(candidate_path)

    return f"ERRORE: File non trovato: '{file_name}'"


def tool_search_files(
    query,
    location=None,
    extensions=None,
    kind=None,
    max_results=25,
    sort=None,
    expand_query=True,
):
    if not query:
        return "ERRORE: Query non valida."

    normalized = query.lower().replace("&", "and")
    normalized = normalized.replace("d&d", "dnd")
    normalized = normalized.replace("d and d", "dnd")
    tokens = [t.strip("-_. ") for t in normalized.split() if t.strip("-_. ")]
    stopwords = {
        "the",
        "my",
        "a",
        "an",
        "of",
        "on",
        "in",
        "to",
        "and",
        "files",
        "file",
        "manual",
        "manuals",
    }
    tokens = [t for t in tokens if t not in stopwords]
    if not tokens:
        tokens = [normalized.strip()]

    everything_path = _get_everything_es_path()
    if not everything_path:
        return "ERRORE: Everything CLI non trovato. Configura EVERYTHING_ES_PATH."

    location_paths = _resolve_search_locations(location)

    variants = _build_everything_variants(query, expand_variants=expand_query)
    use_regex = expand_query and len(variants) > 1
    if use_regex:
        search_expr = _build_everything_regex(query, expand_variants=True)
    else:
        if "&" in query:
            use_regex = True
            search_expr = re.escape(query)
        else:
            search_expr = _build_everything_query(query, expand_variants=False)

    ext_list = []
    if isinstance(extensions, str):
        ext_list = [e.strip().lstrip(".") for e in extensions.split(",") if e.strip()]
    elif isinstance(extensions, list):
        ext_list = [str(e).strip().lstrip(".") for e in extensions if str(e).strip()]

    if ext_list:
        ext_filter = ";".join(ext_list)
        search_expr = f"({search_expr}) ext:{ext_filter}"

    kind_flag = None
    if kind:
        kind_lower = str(kind).strip().lower()
        if kind_lower == "files":
            kind_flag = "/a-d"
        elif kind_lower == "folders":
            kind_flag = "/ad"

    sort_option = None
    if sort:
        sort_option = f"-sort-{sort}"

    try:
        command = [
            everything_path,
            "-full-path-and-name",
            "-n",
            str(max_results),
        ]
        if use_regex:
            command.append("-r")
        if sort_option:
            command.append(sort_option)
        if kind_flag:
            command.append(kind_flag)
        for path in location_paths:
            command.extend(["-path", path])
        command.append(search_expr)

        res = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = (res.stdout or "").strip()
        if res.returncode != 0:
            error_text = (res.stderr or "").strip()
            if error_text:
                logger.error(f"Errore ricerca Everything: {error_text}")
                return f"Errore ricerca Everything: {error_text}"
        if output:
            lines = output.splitlines()
            return "\n".join(lines[:max_results])
    except Exception as e:
        logger.error(f"Errore ricerca Everything: {e}")

    return (
        "Nessun file trovato. Vuoi aprire Everything in modalita interattiva "
        "per affinare la ricerca?"
    )


def tool_open_everything_interactive(query, location=None):
    if not query:
        return "ERRORE: Query non valida."

    gui_path = _get_everything_gui_path()
    if not gui_path:
        return "ERRORE: Everything GUI non trovata. Configura EVERYTHING_GUI_PATH."

    search_expr = _build_everything_query(query, expand_variants=False)
    if not ask_permission("aprire Everything", search_expr, is_dangerous=True):
        return "Utente ha negato l azione."

    try:
        subprocess.Popen([gui_path, "-search", search_expr])
        return "Everything aperto con la ricerca richiesta."
    except Exception as e:
        logger.error(f"Errore apertura Everything: {e}")
        return f"Errore apertura Everything: {e}"

def tool_web_search(query):
    if ask_permission("eseguire ricerca web", query):
        try:
            return "\n".join([str(j) for i, j in enumerate(search(query)) if i < 5])
        except Exception as e:
            logger.error(f"Errore ricerca web: {e}")
            return f"Errore ricerca web: {e}"
    return "Utente ha negato l azione."

def show_diff(filepath, new_content):
    if not os.path.exists(filepath):
        logger.info(f"[NUOVO FILE] {filepath}")
        return
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            old_content = f.readlines()
    except Exception:
        logger.warning("Impossibile leggere originale per diff.")
        return
    new_lines = new_content.splitlines(keepends=True)
    diff = difflib.unified_diff(old_content, new_lines, fromfile=f"a/{filepath}", tofile=f"b/{filepath}")
    logger.info(f"\n=== DIFF: {filepath} ===")
    for line in diff:
        logger.info(line.strip())

def tool_execute(command):
    # Check if the command seems to be a PowerShell command
    is_powershell_command = any(cmdlet in command for cmdlet in ['Get-ItemProperty', 'Set-ItemProperty', 'Get-StartApps'])

    if is_powershell_command:
        # Execute the command using PowerShell
        full_command = f'powershell.exe -NoProfile -Command "{command}"'
    else:
        # Use standard cmd.exe for other commands
        full_command = command

    # Permission is still asked on the original, readable command
    if ask_permission("eseguire comando", command, is_dangerous=True):
        try:
            res = subprocess.run(full_command, shell=True, capture_output=True, text=True, timeout=60)
            out = res.stdout + res.stderr
            return f"Exit Code: {res.returncode}\nOut: {out or '(Nessun output)'}"
        except Exception as e:
            logger.error(f"Errore esecuzione: {e}")
            return f"Errore esecuzione: {e}"
    return "Utente ha negato l azione."


def tool_set_windows_theme(mode):
    if not mode:
        return "ERRORE: Modalita tema non valida."
    mode_lower = mode.strip().lower()
    if mode_lower not in {"light", "dark"}:
        return "ERRORE: Modalita tema non valida. Usa 'light' o 'dark'."
    command = config.LIGHT_THEME_COMMAND if mode_lower == "light" else config.DARK_THEME_COMMAND
    return tool_execute(command)

def tool_read(path):
    if ask_permission("leggere file", path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Errore lettura: {e}")
            return f"Errore lettura: {e}"
    return "Utente ha negato l azione."

from .security import ask_permission

def tool_write(path, content):
    abs_path = os.path.abspath(path)
    if any(abs_path.startswith(os.path.abspath(p)) for p in config.PROTECTED_PATHS):
        logger.warning(f"Accesso negato: tentativo di modificare file protetto: {path}")
        return "ERRORE: Accesso negato. Non puoi modificare i file di progetto."
    if os.path.exists(path): show_diff(path, content)
    if ask_permission("scrivere file", path):
        try:
            with open(path, 'w', encoding='utf-8') as f: f.write(content)
            return f"File scritto con successo: {path}"
        except Exception as e:
            logger.error(f"Errore scrittura: {e}")
            return f"Errore scrittura: {e}"
    return "Utente ha negato l azione."

def tool_list_dir(path, recursive=False):
    if not os.path.exists(path): return "Errore: Percorso non trovato."
    try:
        return "\n".join(os.listdir(path))
    except Exception as e:
        logger.error(f"Errore durante la scansione della directory: {e}")
        return f"Errore durante la scansione: {e}"

def tool_consult_documentation(query):
    logger.debug(f"Consulting documentation with query: '{query}'")
    translator = str.maketrans('', '', string.punctuation)
    raw_tokens = query.lower().split()
    keywords = {token.translate(translator) for token in raw_tokens if token.translate(translator) and token.translate(translator) not in ITALIAN_STOPWORDS}
    
    logger.debug(f"Filtered keywords for search: '{keywords}'")

    if not keywords:
        return "Nessuna corrispondenza trovata (query vuota o solo stopwords)."

    path = "language_docs"
    scored_lines = []
    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        for i, line in enumerate(f):
                            line_lower = line.lower()
                            score = sum(1 for keyword in keywords if keyword in line_lower)
                            if score > 0:
                                scored_lines.append((score, i, f"{filepath}:{i+1}: {line.strip()[:150]}"))
                except Exception as e:
                    logger.debug(f"Could not read or process file {filepath}: {e}")
    except Exception as e:
        logger.error(f"Errore durante la consultazione della documentazione: {e}")
        return f"Errore durante la consultazione della documentazione: {e}"
    
    if not scored_lines:
        return "Nessuna corrispondenza trovata nella documentazione."

    scored_lines.sort(key=lambda x: (-x[0], x[1]))
    
    top_results = [line for score, num, line in scored_lines[:15]]
    
    return "\n".join(top_results)
