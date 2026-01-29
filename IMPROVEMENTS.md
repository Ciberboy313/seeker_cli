# Improvements and Roadmap

## English

This document lists practical improvements aligned with the current codebase and what actually works today.

### Immediate alignment fixes
- Align `docs/windows_hacks.md` with the real commands in `core/config.py`.
- Document that `list_directory` is non-recursive (or implement recursion).
- Fix `direct_test.py` to pass a logger and await `process_input`.
- Make `docs/model_guide.md` match the real tool names and flow.

### Reliability and stability
- Add a max retry limit for invalid JSON responses in `Session`.
- Trim or summarize long history to avoid context overflows.
- Add a consistent timeout for Ollama calls and tool execution.

### Security hardening
- Replace `shell=True` in `tool_execute` with safer command execution.
- Add allowlist or validation for `run_shell_command`.
- Add permission or sanitization for `process_mentions` file injection.
- Constrain read/write access to safe paths or add path allowlists.

### Search and knowledge
- Improve `consult_documentation` with semantic search (embeddings).
- Add caching for documentation search results.

### Test coverage
- Expand tool unit tests (search, open, launch, read/write).
- Add integration tests for router + specialist flow.

## Italiano

Questo documento elenca miglioramenti concreti allineati al codice attuale e a cio che funziona davvero oggi.

### Fix di allineamento immediati
- Allineare `docs/windows_hacks.md` ai comandi reali in `core/config.py`.
- Documentare che `list_directory` non e ricorsivo (o implementare la ricorsione).
- Correggere `direct_test.py` per passare un logger e fare `await process_input`.
- Aggiornare `docs/model_guide.md` con i nomi tool reali e il flow corretto.

### Affidabilita e stabilita
- Aggiungere un limite di retry per JSON non valido in `Session`.
- Ridurre o riassumere la history per evitare overflow del contesto.
- Definire timeout coerenti per Ollama e per i tool.

### Sicurezza
- Rimuovere `shell=True` in `tool_execute` e usare esecuzione sicura.
- Inserire allowlist o validazione per `run_shell_command`.
- Aggiungere permesso o sanitizzazione a `process_mentions`.
- Limitare lettura/scrittura a percorsi sicuri o allowlist.

### Ricerca e conoscenza
- Migliorare `consult_documentation` con ricerca semantica (embeddings).
- Aggiungere caching dei risultati di documentazione.

### Test
- Estendere i test unitari dei tool (search, open, launch, read/write).
- Aggiungere test di integrazione per router + specialist.
