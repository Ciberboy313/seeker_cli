import os
from colorama import Fore, Style

def ask_permission(action, detail, is_dangerous=False):
    """
    Asks the user for permission to perform an action.
    Automatically approves launching executables located in the user's home directory.
    """
    # Auto-approval logic for user-space executables
    if action.upper() == "APRIRE FILE O ESEGUIRE PROGRAMMA" and detail and detail.lower().endswith(('.exe', '.com', '.bat', '.cmd')):
        try:
            user_home = os.path.expanduser('~')
            abs_path = os.path.abspath(detail)
            
            # Check if the absolute path of the executable is within the user's home directory
            if abs_path.startswith(user_home):
                print(f"\n{Fore.GREEN}[AUTO-APPROVATO] Avvio di un'applicazione nello spazio utente:{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{detail}{Style.RESET_ALL}")
                return True
        except Exception:
            # If any error occurs during path checking, fall back to manual confirmation for safety.
            pass

    # Original permission prompt for all other cases
    color = Fore.RED if is_dangerous else Fore.YELLOW
    print(f"\n{color}[PERMESSO RICHIESTO] {action.upper()}{Style.RESET_ALL}")
    if detail:
        print(f"{Fore.CYAN}{detail}{Style.RESET_ALL}")
    
    while True:
        choice = input(f"{Fore.YELLOW}Autorizzi? (y/n): {Style.RESET_ALL}").lower()
        if choice in ['y', 'yes']: return True
        if choice in ['n', 'no']: return False