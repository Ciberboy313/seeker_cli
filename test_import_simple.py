#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test semplice per verificare l'import di tool_write"""

import sys
import os

# Aggiungi la directory corrente al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Test 1: Import core.tools module")
try:
    import core.tools
    print("✓ core.tools importato con successo")
except ImportError as e:
    print(f"✗ Errore import core.tools: {e}")
    sys.exit(1)

print("\nTest 2: Verifica presenza tool_write")
if hasattr(core.tools, 'tool_write'):
    print("✓ tool_write trovato in core.tools")
else:
    print("✗ tool_write NON trovato in core.tools")
    sys.exit(1)

print("\nTest 3: Import diretto di tool_write")
try:
    from core.tools import tool_write
    print("✓ tool_write importato direttamente con successo")
except ImportError as e:
    print(f"✗ Errore import tool_write: {e}")
    sys.exit(1)

print("\nTest 4: Import Session (che usa tool_write)")
try:
    from core.session import Session
    print("✓ Session importato con successo")
except ImportError as e:
    print(f"✗ Errore import Session: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("TUTTI I TEST PASSATI! ✓")
print("="*50)
