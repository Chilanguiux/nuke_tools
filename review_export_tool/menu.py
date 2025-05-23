import nuke
import os
import sys
import subprocess

# Configura tu herramienta
TOOL_NAME = "Review Export Tool"
GITHUB_URL = f"https://github.com/Chilanguiux/nuke_tools.git"
TOOL_DIR = os.path.expanduser(f"~/.nuke/tools/{TOOL_NAME}")
TOOL_ENTRY = "tool"

# Clonar si no existe
if not os.path.exists(TOOL_DIR):
    nuke.message(f"{TOOL_NAME} not found. Cloning from GitHub...")
    try:
        subprocess.run(["git", "clone", GITHUB_URL, TOOL_DIR], check=True)
    except Exception as e:
        nuke.message(f"Error cloning tool: {e}")
else:
    print(f"{TOOL_NAME} ya existe en: {TOOL_DIR}")

# Agregar al sys.path
if TOOL_DIR not in sys.path:
    sys.path.append(TOOL_DIR)

# Importar herramienta
try:
    import importlib
    tool_module = importlib.import_module(TOOL_ENTRY)
except Exception as e:
    nuke.message(f"Error loading tool module: {e}")

# Crear menú en Nuke
toolbar = nuke.menu("Nuke")
menu = toolbar.addMenu("VFX Tools")
menu.addCommand(f"{TOOL_NAME} > Launch", f"{TOOL_ENTRY}.launch()")
