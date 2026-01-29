import sys
import os
sys.path.append(os.getcwd())

print("Importing os", flush=True)
import os
print("Importing subprocess", flush=True)
import subprocess
print("Importing difflib", flush=True)
import difflib
print("Importing colorama", flush=True)
from colorama import Fore, Style
print("Importing security", flush=True)
try:
    from core.security import ask_permission
    print("Imported security", flush=True)
except Exception as e:
    print(f"Failed importing security: {e}", flush=True)

print("Importing datetime", flush=True)
import datetime
print("Importing time", flush=True)
import time
print("Importing threading", flush=True)
import threading
print("Importing queue", flush=True)
import queue

print("Importing tools", flush=True)
try:
    from core.tools import tool_write
    print("Imported tools", flush=True)
except Exception as e:
    print(f"Failed importing tools: {e}", flush=True)

print("Done", flush=True)
