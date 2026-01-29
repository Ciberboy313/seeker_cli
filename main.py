import sys
import os
import asyncio
import logging
from colorama import Fore, Style, init as colorama_init

# Aggiungi la directory corrente al path per importare i moduli
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import core.config
from core.session import Session

try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import PathCompleter
    HAS_TOOLKIT = True
except ImportError:
    HAS_TOOLKIT = False

colorama_init(autoreset=True)

# --- Custom Colored Formatter ---
class ColoredFormatter(logging.Formatter):
    FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    
    LOG_COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.WHITE,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        log_fmt = self.FORMAT
        color = self.LOG_COLORS.get(record.levelno)
        if color:
            log_fmt = color + log_fmt + Style.RESET_ALL
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# --- Configure Logging ---
logger = logging.getLogger('seeker_cli')
logger.setLevel(logging.DEBUG)

# File handler (no colors)
fh = logging.FileHandler('session.log', encoding='utf-8')
fh.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(file_formatter)
logger.addHandler(fh)

# Console handler (with colors)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(ColoredFormatter()) # Use custom colored formatter
logger.addHandler(ch)


async def main():
    logger.info("=== SEEKER CLI ===")
    logger.info("Digita '/help' per i comandi o inizia a chattare.")
    
    if HAS_TOOLKIT:
        prompt_session = PromptSession(completer=PathCompleter())
    
    app_session = Session(logger)

    while True:
        try:
            if HAS_TOOLKIT:
                user_input = await prompt_session.prompt_async("Seeker> ")
            else:
                user_input = input("Seeker> ")
        except (KeyboardInterrupt, EOFError):
            logger.info("Arrivederci!")
            break

        if user_input.lower() in ['exit', 'quit', '/quit']:
            logger.info("Arrivederci!")
            break
            
        await app_session.process_input(user_input)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Sessione interrotta dall'utente.")
    except Exception as e:
        logger.exception("Errore critico non gestito in main.py")