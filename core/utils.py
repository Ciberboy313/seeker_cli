import os
import re
from colorama import Fore, Style

def scan_directory():
    files_list = []
    for root, dirs, files in os.walk("."):
        if ".git" in root or "__pycache__" in root or "node_modules" in root or "seeker_env" in root:
            continue
        for file in files:
            files_list.append(os.path.join(root, file))
    return "\n".join(files_list[:100]) # Limitiamo a 100 file

def process_mentions(user_input):
    pattern = r'@([a-zA-Z0-9_./-]+)'
    matches = re.findall(pattern, user_input)
    
    if not matches: return user_input

    injected = ""
    found = []
    
    for fname in matches:
        path = os.path.abspath(fname) if os.path.exists(fname) else fname
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if len(content) > 12000: 
                        content = content[:12000] + "\n...[TRONCATO]"
                    injected += f"\n\n=== CONTESTO FILE: {fname} ===\n{content}\n============================\n"
                    found.append(fname)
            except: pass
    
    if found:
        print(f"{Fore.GREEN}Letti e allegati: {', '.join(found)}{Style.RESET_ALL}")
        return user_input + injected
    
    return user_input
