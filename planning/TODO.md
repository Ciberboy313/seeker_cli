# Development Plan (Updated)

## English

This plan reflects the current state of the project. Some items below are already implemented and are marked as done.

### Implemented
- Program execution and file opening (`launch_program`, `open_file`, `open_path`).
- File search on Windows via Everything (`search_files`, `open_everything_interactive`).

### Next steps
1. Add max retry limit for invalid JSON in `Session`.
2. Add history trimming or summarization to avoid context overflows.
3. Add permission or sanitization for `process_mentions`.
4. Harden `tool_execute` (remove `shell=True`, add allowlist).
5. Make `list_directory` optionally recursive or update docs only.
6. Fix `direct_test.py` to use async and logger.

## Italiano

Questo piano riflette lo stato attuale del progetto. Alcune voci sono gia implementate e segnate come completate.

### Implementato
- Avvio programmi e apertura file (`launch_program`, `open_file`, `open_path`).
- Ricerca file su Windows con Everything (`search_files`, `open_everything_interactive`).

### Prossimi passi
1. Aggiungere un limite di retry per JSON non valido in `Session`.
2. Ridurre o riassumere la history per evitare overflow del contesto.
3. Aggiungere permesso o sanitizzazione per `process_mentions`.
4. Mettere in sicurezza `tool_execute` (rimuovere `shell=True`, allowlist).
5. Rendere `list_directory` opzionalmente ricorsivo o aggiornare solo la doc.
6. Correggere `direct_test.py` per usare async e logger.
