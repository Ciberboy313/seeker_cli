import json
import logging  # Import the logging module

from colorama import (  # Keep colorama for console if needed, but remove from logger calls
    Fore,
    Style,
)

from . import config
from .llm import call_ollama, clean_json_string
from .router import classify_request
from .tools import (
    tool_consult_documentation,
    tool_execute,
    tool_launch_program,
    tool_list_dir,
    tool_open_path,
    tool_open_file,
    tool_search_files,
    tool_read,
    tool_set_windows_theme,
    tool_web_search,
    tool_write,
    tool_open_everything_interactive,
)
from .utils import process_mentions, scan_directory

# Get the logger instance
logger = logging.getLogger("seeker_cli")



class Session:
    def __init__(self, logger_instance):
        self.logger = logger_instance
        self.history = []
        self.context_files = {}
        self.last_search_context = None
        self.pending_confirmation = None

    def _normalize_run_command(self, user_input, command):
        if not command:
            return command

        prefix = "powershell -command"
        if command.lower().startswith(prefix):
            cleaned = command[len(prefix) :].strip()
            if cleaned.startswith('"') and cleaned.endswith('"'):
                cleaned = cleaned[1:-1]
            return cleaned

        return command

    def _get_tool_names_for_category(self, category):
        category_toolsets = {
            "programming_question": config.PROGRAMMING_TOOLS,
            "system_command": config.SYSTEM_COMMAND_TOOLS,
            "general_chat": config.GENERAL_CHAT_TOOLS,
        }
        selected_toolset = category_toolsets.get(category, config.GENERAL_CHAT_TOOLS)
        return [
            name
            for name, definition in config.TOOL_DEFINITIONS.items()
            if definition in selected_toolset
        ]

    def handle_local_command(self, cmd):
        parts = cmd.split()
        command = parts[0].lower()

        if command == "/init":
            self.logger.info("Scansione directory corrente in corso...")
            scan_result = scan_directory()
            self.logger.info(
                f"Analisi completata. Trovati {len(scan_result.splitlines())} elementi."
            )
            return f"SYSTEM NOTICE: User performed /init. Here is the file structure:\n{scan_result}"

        elif command == "/clear":
            self.context_files.clear()
            self.history = []
            self.logger.info("Memoria e history resettati.")
            return None

        elif command == "/help":
            self.logger.info("=== GUIDA SEEKER ===")
            self.logger.info(
                "1. Usa @nomefile per leggere un file al volo (es. 'Spiegami @main.py')"
            )
            self.logger.info("2. /init : Scansiona la cartella corrente")
            self.logger.info("3. /clear : Pulisce la memoria")
            self.logger.info("4. /quit : Esci")
            return None

        return None

    async def _execute_specialist_loop(self, user_input, tool_names):
        """
        The main reasoning loop, now using a specialist prompt and a limited toolset.
        """
        # Dynamically build the tool list string for the prompt
        tool_definitions = [
            config.TOOL_DEFINITIONS[name]
            for name in tool_names
            if name in config.TOOL_DEFINITIONS
        ]
        tool_list_string = "\n".join(tool_definitions)

        # The first message in history is always the user's input for call_ollama to process
        self.history = [{"role": "user", "content": user_input}]

        self.logger.info(f"({config.MODEL_NAME} sta pensando...)")

        while True:
            # Pass the base prompt and the dynamic tool list to the LLM call
            raw_response = await call_ollama(
                self.history, config.BASE_SPECIALIST_PROMPT, tool_list_string
            )

            try:
                cleaned = clean_json_string(raw_response)
                data = json.loads(cleaned)
            except json.JSONDecodeError:
                self.logger.error(
                    f"Errore formato JSON. Ritento auto-correzione... Raw response: {raw_response}"
                )
                self.history.append({"role": "assistant", "content": raw_response})
                self.history.append(
                    {
                        "role": "user",
                        "content": "Errore: Rispondi SOLO in JSON valido. Correggi il formato.",
                    }
                )
                continue

            action = data.get("action")
            args = data.get("args", {})
            thought = data.get("thought", "")

            if thought:
                self.logger.info(
                    f"{Fore.BLUE}{Style.BRIGHT}Pensiero:{Style.NORMAL} {thought}"
                )

            tool_output = ""
            error_msg = None

            if action not in tool_names:
                error_msg = f"Azione non valida o mancante: '{action}'. Devi usare una delle azioni disponibili per questo ruolo: {', '.join(tool_names)}"
                self.logger.warning(
                    f"Modello ha richiesto azione non consentita: '{action}' per questo specialista."
                )
            else:
                # --- Dispatching Logic ---
                if action == "chat":
                    self.logger.info(f">> {args.get('message')}")
                    self.history.append({"role": "assistant", "content": raw_response})
                    break
                elif action == "finish_task":
                    final_message = args.get("message") or "Task completed successfully."
                    self.logger.info(f">> {final_message}")
                    self.history.append({"role": "assistant", "content": raw_response})
                    break
                # Only call tools that are available to the current specialist
                elif action == "run_shell_command":
                    command = self._normalize_run_command(user_input, args.get("command"))
                    tool_output = tool_execute(command)
                elif action == "read_file":
                    tool_output = tool_read(args.get("file_path"))
                elif action == "write_file":
                    tool_output = tool_write(args.get("file_path"), args.get("content"))
                elif action == "open_path":
                    tool_output = tool_open_path(args.get("path"))
                elif action == "open_file":
                    tool_output = tool_open_file(
                        args.get("file_name"),
                        args.get("location"),
                        args.get("program_name"),
                    )
                elif action == "search_files":
                    self.last_search_context = {
                        "query": args.get("query"),
                        "location": args.get("location"),
                    }
                    tool_output = tool_search_files(
                        args.get("query"),
                        args.get("location"),
                        args.get("extensions"),
                        args.get("kind"),
                        args.get("max_results", 25),
                        args.get("sort"),
                        args.get("expand_query", True),
                    )
                    if isinstance(tool_output, str) and tool_output.startswith(
                        "Nessun file trovato"
                    ):
                        self.pending_confirmation = {
                            "action": "open_everything_interactive",
                            "query": args.get("query"),
                            "location": args.get("location"),
                        }
                elif action == "open_everything_interactive":
                    tool_output = tool_open_everything_interactive(
                        args.get("query"), args.get("location")
                    )
                elif action == "launch_program":
                    tool_output = tool_launch_program(args.get("program_name"))
                elif action == "set_windows_theme":
                    tool_output = tool_set_windows_theme(args.get("mode"))
                elif action == "list_directory":
                    tool_output = tool_list_dir(
                        args.get("dir_path", "."), args.get("recursive", False)
                    )
                elif action == "google_web_search":
                    tool_output = tool_web_search(args.get("query"))
                elif action == "consult_documentation":
                    tool_output = tool_consult_documentation(args.get("query"))

            if error_msg:
                self.logger.error(f"[ERRORE]: {error_msg} Ritento...")
                self.history.append({"role": "assistant", "content": raw_response})
                self.history.append(
                    {
                        "role": "user",
                        "content": f"Errore: {error_msg}. Correggi la tua risposta JSON.",
                    }
                )
                continue

            # Feedback Loop
            self.history.append({"role": "assistant", "content": raw_response})
            self.logger.info(
                f"{Fore.MAGENTA}[SYSTEM]: Risultato azione '{action}': {str(tool_output)[:300]}..."
            )
            self.history.append(
                {
                    "role": "user",
                    "content": f"Risultato azione '{action}': {tool_output}",
                }
            )

    async def process_input(self, user_input):
        if user_input.startswith("/"):
            sys_msg = self.handle_local_command(user_input)
            if sys_msg:
                self.history.append({"role": "user", "content": sys_msg})
            return

        processed_input = process_mentions(user_input)

        if self.pending_confirmation:
            normalized = processed_input.strip().lower()
            if normalized in {"y", "yes", "si", "sì", "ok"}:
                action = self.pending_confirmation.get("action")
                if action == "open_everything_interactive":
                    tool_output = tool_open_everything_interactive(
                        self.pending_confirmation.get("query"),
                        self.pending_confirmation.get("location"),
                    )
                    self.logger.info(
                        f"{Fore.MAGENTA}[SYSTEM]: Risultato azione 'open_everything_interactive': {str(tool_output)[:300]}..."
                    )
                    self.pending_confirmation = None
                    return
            if normalized in {"n", "no"}:
                self.pending_confirmation = None
                self.logger.info(">> Ok, non apro Everything. Dimmi come vuoi affinare la ricerca.")
                return

        if self.last_search_context:
            short_followup = len(processed_input.split()) <= 4
            if short_followup:
                augmented = (
                    "Follow-up to a file search request. "
                    f"Previous query: {self.last_search_context.get('query')}. "
                    f"Previous location: {self.last_search_context.get('location')}. "
                    f"New input: {processed_input}"
                )
                processed_input = augmented

        category = classify_request(processed_input)
        self.logger.info(
            f"{Fore.YELLOW}Richiesta classificata come: {category}{Style.RESET_ALL}"
        )

        if category == "programming_question":
            self.logger.info(
                f"{Fore.CYAN}(Cerco nella documentazione locale...){Style.RESET_ALL}"
            )
            doc_results = tool_consult_documentation(processed_input)

            augmented_input = f"""L'utente ha chiesto: '{processed_input}'

--- INIZIO DOCUMENTAZIONE ---
{doc_results}
--- FINE DOCUMENTAZIONE ---

Analizza i risultati della documentazione qui sopra. Se contengono informazioni pertinenti, anche se non è un esempio perfetto, **usa la tua conoscenza per sintetizzare la risposta corretta e forniscila all'utente usando il tool 'chat' o 'finish_task'**. Non usare `consult_documentation` di nuovo se hai già trovato informazioni pertinenti. Usa altri tool (come `google_web_search`) solo se la documentazione è completamente irrilevante.
"""
            tool_names = self._get_tool_names_for_category(category)
            await self._execute_specialist_loop(augmented_input, tool_names)

        elif category == "system_command":
            tool_names = self._get_tool_names_for_category(category)
            await self._execute_specialist_loop(processed_input, tool_names)

        else:  # general_chat
            tool_names = self._get_tool_names_for_category(category)
            await self._execute_specialist_loop(processed_input, tool_names)
