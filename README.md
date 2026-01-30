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
- Ollama installed and running (from the official site).
- Ollama models pulled: `gemma2:2b` and `llama3.2:1b`.
- Windows for `search_files`, `open_everything_interactive`, and theme control.
- Everything installed for file search from the official site (CLI: `es.exe`, GUI: `Everything.exe`).

### Ollama and LLM Models
Ollama lets you run language models locally.

| Item | Description | Install / Command |
| --- | --- | --- |
| Ollama (software) | Main application to manage and run models. | https://ollama.com/download |
| Gemma 2 (2b) | Lightweight model for quick tasks. | `ollama run gemma2:2b` |
| Llama 3.2 (1b) | Ultra-compact model for low resources. | `ollama run llama3.2:1b` |

Note: Install Ollama first. Then open a terminal (PowerShell or Command Prompt) and run the commands above.

### Everything (voidtools)
Everything is a fast file indexer for Windows.

| Item | Description | Download |
| --- | --- | --- |
| Everything (GUI) | Standard graphical interface. | https://www.voidtools.com/downloads/ |
| Everything CLI (es.exe) | Command-line search tool. | https://www.voidtools.com/downloads/ |

How to configure the CLI (`es.exe`):
1. Download the `.zip` file.
2. Extract `es.exe` to a folder of your choice.
3. Optional: add that folder to your system `PATH`.
4. Keep Everything GUI running in the background.

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
- Ollama installato e in esecuzione (dal sito ufficiale).
- Modelli Ollama scaricati: `gemma2:2b` e `llama3.2:1b`.
- Windows per `search_files`, `open_everything_interactive` e gestione tema.
- Everything installato per la ricerca file dal sito ufficiale (CLI: `es.exe`, GUI: `Everything.exe`).

### Ollama e Modelli LLM
Ollama permette di eseguire modelli di linguaggio localmente.

| Oggetto | Descrizione | Link / Comando |
| --- | --- | --- |
| Ollama (software) | Applicazione principale per gestire ed eseguire i modelli. | https://ollama.com/download |
| Gemma 2 (2b) | Modello leggero per compiti rapidi. | `ollama run gemma2:2b` |
| Llama 3.2 (1b) | Modello ultra compatto per risorse limitate. | `ollama run llama3.2:1b` |

Nota: installa prima Ollama. Poi apri il terminale (PowerShell o Prompt dei comandi) ed esegui i comandi sopra.

### Everything (voidtools)
Everything e un motore di ricerca file veloce per Windows.

| Oggetto | Descrizione | Download |
| --- | --- | --- |
| Everything (GUI) | Versione con interfaccia grafica. | https://www.voidtools.com/downloads/ |
| Everything CLI (es.exe) | Versione a riga di comando. | https://www.voidtools.com/downloads/ |

Come configurare la CLI (`es.exe`):
1. Scarica il file `.zip`.
2. Estrai `es.exe` in una cartella a tua scelta.
3. Opzionale: aggiungi la cartella al `PATH` di sistema.
4. Tieni Everything GUI aperto in background.

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
