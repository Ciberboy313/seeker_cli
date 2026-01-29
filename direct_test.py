import sys
import os
from colorama import Fore, Style, init as colorama_init
from core.session import Session
import core.config

def run_direct_test(model_name, prompts):
    """
    Esegue un test non interattivo del bot.
    """
    colorama_init(autoreset=True)
    print(f"{Fore.MAGENTA}=== DIRECT TEST ==={Style.RESET_ALL}")

    # Imposta il modello
    core.config.MODEL_NAME = model_name
    print(f"{Fore.GREEN}Modello in uso: {core.config.MODEL_NAME}{Style.RESET_ALL}")

    session = Session()

    for i, prompt in enumerate(prompts):
        print(f"\n{Fore.YELLOW}[INPUT {i+1}]{Style.RESET_ALL} {prompt}")
        session.process_input(prompt)

    print(f"\n\n{Fore.MAGENTA}=== STORIA CONVERSAZIONE FINALE ==={Style.RESET_ALL}")
    import json
    print(json.dumps(session.history, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    # Esempio di test case
    test_prompts = [
        "Ciao, scrivimi un file sul desktop chiamato 'test.txt' con dentro la scritta 'test superato'.",
        "Ora leggimi il file 'test.txt' che hai creato sul desktop.",
        "Perfetto, ora cancellalo."
    ]
    # Puoi cambiare il modello qui se vuoi testarne un altro
    # model_to_test = "codellama:7b" 
    model_to_test = "deepseek-coder:6.7b"
    
    run_direct_test(model_to_test, test_prompts)
