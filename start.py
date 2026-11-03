#!/usr/bin/env python3
"""Launcher cross-platform para interface.py (Linux, macOS, Windows)."""
import os, sys, subprocess, platform

DIR = os.path.dirname(os.path.abspath(__file__))
venv_py = (
    os.path.join(DIR, "venv", "Scripts", "python.exe")
    if platform.system() == "Windows"
    else os.path.join(DIR, "venv", "bin", "python")
)
interface = os.path.join(DIR, "interface.py")

if not os.path.isfile(venv_py):
    print("Venv nao encontrado. Execute:")
    if platform.system() == "Windows":
        print("  python -m venv venv")
        print("  venv\\Scripts\\pip install -r requirements.txt")
    else:
        print("  python3 -m venv venv && venv/bin/pip install -r requirements.txt")
    sys.exit(1)

subprocess.run([venv_py, interface])
