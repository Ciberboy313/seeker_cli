# Gemini Agent Context: Seeker CLI

## English

### Note
My available tools are those provided by this environment. The tools described below (like `finish_task` or `launch_program`) belong to the Seeker CLI application I am documenting. I must not call those tools directly.

### Project overview
Seeker CLI is a command-line AI assistant built in Python. It uses Ollama for LLM calls, routes requests via a router-specialist flow, and executes tool actions from `core/tools.py` through `core/session.py`.

### Default models
The current defaults in `core/config.py` and `.env.example` are:
- Specialist: `gemma2:2b`
- Router: `llama3.2:1b`

### Build and run
```bash
pip install -r requirements.txt
python main.py
```

### Tests
```bash
python -m unittest discover tests
```

### Target application tools (Seeker LLM)
- `run_shell_command`
- `read_file`, `write_file`
- `list_directory`
- `search_files`, `open_everything_interactive`
- `open_file`, `open_path`
- `launch_program`
- `set_windows_theme`
- `consult_documentation`
- `google_web_search`
- `chat`, `finish_task`

### Security note
`core/security.py` prompts the user before potentially dangerous actions, but `process_mentions` currently injects file content without a permission check.

## Italiano

### Nota
I tool disponibili per me sono quelli dell ambiente. I tool elencati qui (es. `finish_task`, `launch_program`) appartengono all app Seeker CLI che sto documentando. Non devo chiamarli direttamente.

### Panoramica
Seeker CLI e un assistente AI da riga di comando in Python. Usa Ollama per le chiamate LLM, instrada le richieste con router-specialist e usa i tool in `core/tools.py` tramite `core/session.py`.

### Modelli di default
I default attuali in `core/config.py` e `.env.example` sono:
- Specialist: `gemma2:2b`
- Router: `llama3.2:1b`

### Build e avvio
```bash
pip install -r requirements.txt
python main.py
```

### Test
```bash
python -m unittest discover tests
```

### Tool dell applicazione target (Seeker LLM)
- `run_shell_command`
- `read_file`, `write_file`
- `list_directory`
- `search_files`, `open_everything_interactive`
- `open_file`, `open_path`
- `launch_program`
- `set_windows_theme`
- `consult_documentation`
- `google_web_search`
- `chat`, `finish_task`

### Nota sicurezza
`core/security.py` chiede conferma prima di azioni potenzialmente pericolose, ma `process_mentions` inietta contenuto senza chiedere permesso.
