# Seeker CLI

## English

Seeker CLI is a command-line AI assistant that runs locally and uses Ollama to interpret requests and execute tasks through a tool-based system.

### Features
- Router + specialist LLM flow with tool gating.
- Local documentation search (keyword-based) via `language_docs/`.
- File search using Everything CLI (Windows only).
- Program launch and file open helpers (Windows).
- Permission prompts for potentially dangerous actions.

### Requirements
- Python 3.8+.
- Ollama installed and running.
- Windows for `search_files`, `open_everything_interactive`, and theme control.
- Everything installed for file search (CLI: `es.exe`, GUI: `Everything.exe`).

### Install
```bash
pip install -r requirements.txt
```

### Configuration
Create `.env` (see `.env.example`) to override defaults.

```text
OLLAMA_URL=http://localhost:11434/api/chat
MODEL_NAME=gemma2:2b
ROUTER_MODEL_NAME=llama3.2:1b
EVERYTHING_ES_PATH=C:\Program Files\Everything\es.exe
EVERYTHING_GUI_PATH=C:\Program Files\Everything\Everything.exe
```

### Run
```bash
python main.py
```

### Tests
```bash
python -m unittest discover tests
```

### Notes and limitations
- `list_directory` is non-recursive even if `recursive=true` is passed.
- `consult_documentation` is keyword-based, not semantic.
- `search_files` relies on Everything being installed and running.
- `process_mentions` (`@file`) injects file content without a permission prompt.

### Versioning
- Current version in `VERSION`.
- Release notes in `CHANGELOG.md`.

## Italiano

Seeker CLI e un assistente AI da riga di comando che gira in locale e usa Ollama per interpretare le richieste e eseguire task con un sistema di tool.

### Funzionalita
- Flusso router + specialist con tool limitati.
- Ricerca documentazione locale (keyword-based) in `language_docs/`.
- Ricerca file con Everything CLI (solo Windows).
- Apertura programmi e file (Windows).
- Conferma utente per azioni potenzialmente pericolose.

### Requisiti
- Python 3.8+.
- Ollama installato e in esecuzione.
- Windows per `search_files`, `open_everything_interactive` e gestione tema.
- Everything installato per la ricerca file (CLI: `es.exe`, GUI: `Everything.exe`).

### Installazione
```bash
pip install -r requirements.txt
```

### Configurazione
Crea `.env` (vedi `.env.example`) per sovrascrivere i default.

```text
OLLAMA_URL=http://localhost:11434/api/chat
MODEL_NAME=gemma2:2b
ROUTER_MODEL_NAME=llama3.2:1b
EVERYTHING_ES_PATH=C:\Program Files\Everything\es.exe
EVERYTHING_GUI_PATH=C:\Program Files\Everything\Everything.exe
```

### Avvio
```bash
python main.py
```

### Test
```bash
python -m unittest discover tests
```

### Note e limiti
- `list_directory` non e ricorsivo anche se `recursive=true`.
- `consult_documentation` e basato su keyword, non semantico.
- `search_files` richiede Everything installato e in funzione.
- `process_mentions` (`@file`) inietta contenuto senza richiesta di permesso.

### Versioni
- Versione corrente in `VERSION`.
- Note di rilascio in `CHANGELOG.md`.
