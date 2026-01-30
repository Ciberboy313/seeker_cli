# Plan to Fix Critical Issues

## English

This document lists the known issues and a concrete plan to address them, starting from the highest priority items.

### 1) Insecure Shell Command Execution (`core/tools.py: tool_execute`)
**Goal:** remove `shell=True` and reduce arbitrary execution.

**Plan:**
- Split handling for PowerShell vs normal executables.
- PowerShell: use `subprocess.run(["powershell.exe", "-NoProfile", "-Command", command], shell=False, ...)`.
- Non-PowerShell: use `shell=False` with parsing (`shlex.split(..., posix=False)`) and block metacharacters (`& | && || > < ;`).
- Add an allowlist of safe executables (`git`, `python`, `pip`, `ollama`, etc.).
- Add configurable timeout and keep full output in logs.

**Tests:**
- Command with `&&` or `|` is rejected.
- PowerShell command runs via `shell=False`.
- Read-only commands like `python --version` work.

---

### 2) Prompt Injection via Context (`core/utils.py: process_mentions`)
**Goal:** prevent unsafe file injection via `@file` mentions.

**Plan:**
- Ask permission before reading/injecting each file.
- Enforce per-file and total context size limits.
- Sanitize prompt-like patterns and wrap content as untrusted.
- Optionally disable mentions by default or restrict to safe roots.

**Tests:**
- Malicious file strings do not alter system prompt.
- Oversized file is truncated and flagged.

---

### 3) Infinite JSON Loop (`core/session.py`)
**Goal:** stop infinite retries on invalid JSON.

**Plan:**
- Add `MAX_JSON_RETRIES` (3-5).
- After max retries, return a user-facing error and exit loop.
- Log raw invalid responses for debugging.

**Tests:**
- Mock invalid JSON -> loop stops after N tries.
- Second try valid JSON -> continues normally.

---

### 4) Unlimited History Growth (`core/session.py`)
**Goal:** prevent unbounded memory and token growth.

**Plan:**
- Trim history to a fixed size (e.g., last 40 messages).
- Always keep last user request and tool results.
- Optional: summarize older history.

**Tests:**
- After 200 entries, history length stays <= limit.

---

### 5) Encoding/Unicode Read Errors (`tool_read`, `process_mentions`, `show_diff`)
**Goal:** read files safely without crashes.

**Plan:**
- Try UTF-8, then fallback encodings (e.g., cp1252).
- Detect binary files and return a safe message.
- Update `show_diff` to use safe read.

**Tests:**
- cp1252 file is readable.
- Binary file returns a placeholder message.

---

### 6) Python REPL Vulnerability
**Status:** not applicable in this codebase (no Python REPL tool).

**If added later:**
- Sandbox, allowlist imports, enforce timeouts, isolate process.

---

### 7) Unlimited File System Access (`tool_read`, `tool_write`, `open_path`)
**Goal:** restrict access to safe paths.

**Plan:**
- Define `SAFE_READ_ROOTS` and `SAFE_WRITE_ROOTS`.
- Normalize paths and block traversal outside roots.
- Block sensitive files by default (`.env`, credentials, system dirs).
- Require explicit confirmation for dangerous paths.

**Tests:**
- `../.env` blocked.
- Desktop file allowed.

---

### 8) Missing Logging and Audit Trail
**Goal:** add structured audit logs.

**Plan:**
- Add `audit.log` (JSON lines or structured text).
- Log every permission request (approved/denied).
- Log every tool execution with arguments and exit code.
- Redact sensitive paths/values.

**Tests:**
- Tool call generates an audit entry.
- Denied permission logged as `denied`.

---

### 9) Unpinned Dependencies (`requirements.txt`)
**Goal:** improve reproducibility.

**Plan:**
- Pin versions or create `requirements.lock`.
- Document update process.

**Tests:**
- Clean install in venv succeeds.

---

### 10) Mutable System Prompt (`core/config.py`)
**Goal:** reduce accidental modification risk.

**Plan:**
- Move prompts to frozen constants or read-only files.
- Validate dynamic sections before interpolation.

**Tests:**
- Prompt always contains required headers.

---

### 11) Generic Error Handling
**Goal:** more useful error reporting.

**Plan:**
- Replace broad `except Exception` with specific exceptions.
- Log stack traces only for unexpected failures.

---

### 12) Non-Global Timeout Policy
**Goal:** consistent timeouts.

**Plan:**
- Centralize timeouts in `core/config.py`.
- Apply to requests, subprocess, and file I/O.

---

### 13) No Input Validation
**Goal:** reject unsafe or huge input.

**Plan:**
- Cap input length (e.g., 4000-10000 chars).
- Normalize whitespace and control characters.

---

### 14) State Consistency
**Goal:** align working directories and tool behavior.

**Plan:**
- Define a workspace root.
- Ensure `run_shell_command` uses `dir_path` if provided.

---

### 15) Output Truncation
**Goal:** keep UX readable without losing data.

**Plan:**
- Show first N lines + truncation notice.
- Log full output or write to a temp file.

---

### 16) Disorganized Imports
**Goal:** standardize imports.

**Plan:**
- Reorder imports (stdlib, third-party, local).
- Optionally use ruff/isort.

---

### 17) Missing Docstrings
**Goal:** document tool contracts.

**Plan:**
- Add docstrings to public functions (args, return, side effects).

---

### 18) Missing Type Hints
**Goal:** reduce bugs and improve tooling.

**Plan:**
- Add type hints to public functions and main data structures.
- Optional: introduce `mypy` checks.

---

### 19) Version Control Info
**Status:** resolved (repo, `.gitignore`, `VERSION`, `CHANGELOG.md`).

---

### 20) Magic Numbers
**Goal:** centralize constants.

**Plan:**
- Move limits and defaults into `core/config.py`.
- Reference constants in code paths.

---

## Italiano

Questo documento elenca i problemi noti e un piano concreto per risolverli, partendo dalle priorita piu alte.

### 1) Esecuzione comandi non sicura (`core/tools.py: tool_execute`)
**Obiettivo:** eliminare `shell=True` e ridurre l esecuzione arbitraria.

**Piano:**
- Separare PowerShell da eseguibili normali.
- PowerShell: `subprocess.run(["powershell.exe", "-NoProfile", "-Command", command], shell=False, ...)`.
- Non-PowerShell: `shell=False` con parsing (`shlex.split(..., posix=False)`) e blocco metacaratteri (`& | && || > < ;`).
- Allowlist di eseguibili sicuri (`git`, `python`, `pip`, `ollama`, ecc.).
- Timeout configurabile e output completo nei log.

**Test:**
- Comando con `&&` o `|` rifiutato.
- Comando PowerShell valido funziona senza shell.
- Comandi read-only come `python --version` funzionano.

---

### 2) Prompt Injection da contesto (`core/utils.py: process_mentions`)
**Obiettivo:** evitare iniezioni via `@file`.

**Piano:**
- Chiedere permesso prima di leggere/iniettare ogni file.
- Limitare dimensione per file e dimensione totale.
- Sanitizzare pattern pericolosi e marcatura come contenuto non fidato.
- Opzionale: disabilitare per default o limitare a percorsi sicuri.

**Test:**
- File malevolo non altera il system prompt.
- File enorme viene troncato e marcato.

---

### 3) Loop JSON infinito (`core/session.py`)
**Obiettivo:** fermare retry infiniti.

**Piano:**
- Aggiungere `MAX_JSON_RETRIES` (3-5).
- Dopo il limite, messaggio d errore e uscita dal loop.
- Log dei raw response invalidi.

**Test:**
- JSON invalido -> stop dopo N tentativi.
- JSON valido al secondo tentativo -> ok.

---

### 4) History illimitata (`core/session.py`)
**Obiettivo:** evitare crescita senza limite.

**Piano:**
- Trim della history (es. ultime 40 entries).
- Mantenere ultime richieste e risultati tool.
- Opzionale: summary dei messaggi vecchi.

**Test:**
- Dopo 200 entries, history <= limite.

---

### 5) Errori encoding/Unicode (`tool_read`, `process_mentions`, `show_diff`)
**Obiettivo:** leggere file senza crash.

**Piano:**
- Fallback encoding (cp1252 ecc.).
- Rilevare binari e restituire messaggio sicuro.
- Aggiornare `show_diff` con lettura sicura.

**Test:**
- File cp1252 leggibile.
- File binario -> placeholder.

---

### 6) Vulnerabilita Python REPL
**Stato:** non applicabile (nessun REPL in questa codebase).

**Se aggiunto:**
- Sandbox, allowlist import, timeout, processo isolato.

---

### 7) Accesso FS illimitato (`tool_read`, `tool_write`, `open_path`)
**Obiettivo:** limitare percorsi.

**Piano:**
- Definire `SAFE_READ_ROOTS` e `SAFE_WRITE_ROOTS`.
- Normalizzare path e bloccare traversal.
- Bloccare file sensibili per default.
- Conferma esplicita per percorsi pericolosi.

**Test:**
- `../.env` bloccato.
- File sul Desktop consentito.

---

### 8) Logging e audit trail
**Obiettivo:** log strutturato delle azioni.

**Piano:**
- Aggiungere `audit.log`.
- Loggare richieste permesso e risultati.
- Loggare tool con argomenti e exit code.
- Redazione valori sensibili.

**Test:**
- Ogni tool genera una riga audit.
- Permission denied tracciato.

---

### 9) Dipendenze non bloccate (`requirements.txt`)
**Obiettivo:** build riproducibile.

**Piano:**
- Pin versioni o `requirements.lock`.
- Documentare la procedura di update.

---

### 10) Prompt di sistema mutabile (`core/config.py`)
**Obiettivo:** ridurre modifiche accidentali.

**Piano:**
- Prompt in costanti immutabili o file di sola lettura.
- Validare le sezioni dinamiche.

---

### 11) Error handling generico
**Obiettivo:** errori piu chiari.

**Piano:**
- Eccezioni specifiche per I/O, subprocess, requests.
- Stacktrace solo per errori non previsti.

---

### 12) Timeout incoerenti
**Obiettivo:** timeouts coerenti.

**Piano:**
- Centralizzare timeouts in `core/config.py`.
- Applicarli a requests, subprocess e I/O.

---

### 13) Nessuna validazione input
**Obiettivo:** evitare crash/abusi input.

**Piano:**
- Limitare lunghezza input.
- Normalizzare whitespace e caratteri di controllo.

---

### 14) Consistenza dello stato
**Obiettivo:** coerenza tra tool e working directory.

**Piano:**
- Definire un workspace root.
- Usare `dir_path` in `run_shell_command`.

---

### 15) Troncamento output
**Obiettivo:** UX leggibile senza perdere dati.

**Piano:**
- Mostrare N righe + messaggio di truncation.
- Log completo o file temporaneo.

---

### 16) Import disordinati
**Obiettivo:** manutenzione.

**Piano:**
- Ordinare import (stdlib, third-party, local).
- Usare ruff/isort se vuoi.

---

### 17) Docstring mancanti
**Obiettivo:** documentare i tool.

**Piano:**
- Aggiungere docstring a funzioni pubbliche.

---

### 18) Type hints mancanti
**Obiettivo:** ridurre bug.

**Piano:**
- Aggiungere type hints a funzioni e strutture.
- Opzionale: `mypy`.

---

### 19) Versioning
**Stato:** risolto (repo, `.gitignore`, `VERSION`, `CHANGELOG.md`).

---

### 20) Magic numbers
**Obiettivo:** centralizzare costanti.

**Piano:**
- Spostare limiti e default in `core/config.py`.
- Usare costanti nel codice.
