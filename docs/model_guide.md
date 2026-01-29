# Operational Guide for Seeker CLI Models

## English

This guide documents the tool names and behaviors that actually exist in this codebase. Use it when editing prompts or describing tool behavior.

### File system and search
- Prefer `list_directory` instead of shell commands.
- `list_directory` is non-recursive.
- Use `search_files` for filename search via Everything (Windows only).
- If `search_files` finds nothing, ask the user before using `open_everything_interactive`.

### Reading and writing
- Use `read_file` and `write_file` for file access.
- Both actions require user confirmation.

### System actions
- Use `launch_program` or `open_path` to open apps/files.
- Use `set_windows_theme` for theme changes.
- Use `run_shell_command` only when a specific tool does not exist.

### Knowledge lookup
- `consult_documentation` is keyword-based and reads `language_docs/`.
- Use `google_web_search` only if local docs are irrelevant.

### Conversation flow
- `chat` communicates with the user.
- `finish_task` ends a completed task.

### Available tools (summary)
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

## Italiano

Questa guida documenta i nomi e i comportamenti dei tool reali in questo codice. Usala quando modifichi prompt o descrizioni dei tool.

### File system e ricerca
- Preferisci `list_directory` ai comandi shell.
- `list_directory` non e ricorsivo.
- Usa `search_files` per la ricerca nomi file via Everything (solo Windows).
- Se `search_files` non trova nulla, chiedi conferma prima di `open_everything_interactive`.

### Lettura e scrittura
- Usa `read_file` e `write_file` per accedere ai file.
- Entrambe richiedono conferma utente.

### Azioni di sistema
- Usa `launch_program` o `open_path` per aprire app/file.
- Usa `set_windows_theme` per il tema.
- Usa `run_shell_command` solo se non esiste un tool dedicato.

### Ricerca conoscenza
- `consult_documentation` e keyword-based su `language_docs/`.
- Usa `google_web_search` solo se la doc locale e irrilevante.

### Flusso conversazionale
- `chat` comunica con l utente.
- `finish_task` chiude il task completato.

### Tool disponibili (summary)
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
