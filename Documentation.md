# Seeker CLI Documentation

## English

### Overview
Seeker CLI is a local command-line AI assistant that uses Ollama to interpret user requests and execute tasks through a tool-based loop.

### Architecture
- Router + specialist flow: a router classifies the request, then a specialist prompt with a limited toolset handles it.
- Tool execution loop: the model responds in JSON with an action; the app executes the tool and feeds the result back to the model.
- Logging: console output is colored, and all activity is written to `session.log`.

### Configuration
Main settings are in `core/config.py`, with overrides via `.env`.

Key values:
- `OLLAMA_URL`, `MODEL_NAME`, `ROUTER_MODEL_NAME`
- `EVERYTHING_ES_PATH`, `EVERYTHING_GUI_PATH`
- `ROUTER_TIMEOUT`, `ROUTER_CONFIDENCE_THRESHOLD`
- `PROTECTED_PATHS`, `CUSTOM_PROGRAM_PATHS`

### Tools and capabilities
The specialist can call these actions (tool names are internal, user sees natural language):
- `run_shell_command`: run a command (requires confirmation).
- `read_file`, `write_file`: read/write files (confirmation required).
- `list_directory`: list a directory (non-recursive).
- `search_files`: search by name via Everything CLI (Windows only).
- `open_everything_interactive`: open Everything GUI with a query.
- `open_file`, `open_path`: open files or folders.
- `launch_program`: find and launch executables.
- `set_windows_theme`: light/dark theme commands.
- `consult_documentation`: keyword search in `language_docs/`.
- `google_web_search`: web search (with confirmation).
- `chat`, `finish_task`: user-facing responses.

### Current behavior (verified)
- The REPL starts via `python main.py` and logs to `session.log`.
- Router classification works with heuristic + LLM fallback.
- Ollama endpoint is contacted for router and specialist prompts.
- Everything integration works when `es.exe` is installed and configured.
- RAG is keyword-based and returns line matches, not semantic chunks.

### Known limitations
- `list_directory` ignores `recursive=true`.
- `process_mentions` (`@file`) injects file content without a permission prompt.
- `tool_execute` uses `shell=True` and should be hardened.
- Router retry loop has no max retry limit and history can grow without trimming.
- Some docs were previously inconsistent with code (now aligned).

### Related docs
- `IMPROVEMENTS.md`: roadmap and proposed fixes.
- `CRITIC_CONSIDERATION.md`: security and stability risks.
- `docs/windows_hacks.md`: cookbook commands for Windows theme.
- `VERSION`: current version.
- `CHANGELOG.md`: release notes.

## Italiano

### Panoramica
Seeker CLI e un assistente AI locale da riga di comando che usa Ollama per interpretare le richieste ed eseguire task tramite un loop di tool.

### Architettura
- Flusso router + specialist: il router classifica la richiesta, poi uno specialist con tool limitati la gestisce.
- Loop tool: il modello risponde in JSON con un azione; l app esegue il tool e rimanda il risultato al modello.
- Logging: output colorato in console e log completo in `session.log`.

### Configurazione
Le impostazioni principali sono in `core/config.py`, con override via `.env`.

Valori principali:
- `OLLAMA_URL`, `MODEL_NAME`, `ROUTER_MODEL_NAME`
- `EVERYTHING_ES_PATH`, `EVERYTHING_GUI_PATH`
- `ROUTER_TIMEOUT`, `ROUTER_CONFIDENCE_THRESHOLD`
- `PROTECTED_PATHS`, `CUSTOM_PROGRAM_PATHS`

### Tool e capacita
Lo specialist puo chiamare queste azioni (nomi interni, l utente usa linguaggio naturale):
- `run_shell_command`: esegue comandi (con conferma).
- `read_file`, `write_file`: lettura/scrittura file (conferma).
- `list_directory`: lista directory (non ricorsivo).
- `search_files`: ricerca con Everything CLI (solo Windows).
- `open_everything_interactive`: apre Everything GUI con query.
- `open_file`, `open_path`: apre file o cartelle.
- `launch_program`: trova e avvia eseguibili.
- `set_windows_theme`: cambia tema light/dark.
- `consult_documentation`: ricerca keyword in `language_docs/`.
- `google_web_search`: ricerca web (con conferma).
- `chat`, `finish_task`: risposte all utente.

### Comportamento attuale (verificato)
- La REPL parte con `python main.py` e logga in `session.log`.
- La classificazione router funziona con euristica + fallback LLM.
- Ollama viene chiamato per router e specialist.
- Everything funziona quando `es.exe` e configurato.
- Il RAG e basato su keyword, non semantico.

### Limiti noti
- `list_directory` ignora `recursive=true`.
- `process_mentions` (`@file`) inietta contenuto senza conferma.
- `tool_execute` usa `shell=True` e va messo in sicurezza.
- Il loop JSON non ha max retry e la history cresce senza limite.
- Alcune doc erano incoerenti con il codice (ora allineate).

### Documenti correlati
- `IMPROVEMENTS.md`: roadmap e fix proposti.
- `CRITIC_CONSIDERATION.md`: rischi security/stability.
- `docs/windows_hacks.md`: comandi cookbook per il tema.
- `VERSION`: versione corrente.
- `CHANGELOG.md`: note di rilascio.
