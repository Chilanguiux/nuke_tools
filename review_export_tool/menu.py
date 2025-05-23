import os
import sys
import subprocess
import nuke

# Setup tool
TOOL_NAME = "Review Export Tool"
GITHUB_URL = f"https://github.com/Chilanguiux/nuke_tools.git"
TOOL_DIR = os.path.expanduser(f"~/.nuke/tools/{TOOL_NAME}")

# Clone repo if dont exists
if not os.path.exists(TOOL_DIR):
    nuke.message(f"{TOOL_NAME} not found. Cloning from GitHub...")
    try:
        subprocess.run(["git", "clone", GITHUB_URL, TOOL_DIR], check=True)
    except Exception as e:
        nuke.message(f"Error cloning tool: {e}")
else:
    print(f"{TOOL_NAME} ya existe en: {TOOL_DIR}")

# Adding to sys.path
if TOOL_DIR not in sys.path:
    sys.path.append(TOOL_DIR)

# Importing tool
try:
    import tool
    import importlib
    TOOL_ENTRY = "tool"
    tool_module = importlib.import_module(TOOL_ENTRY)
except Exception as e:
    nuke.message(f"Error loading tool module: {e}")

# Nuke menu setup
toolbar = nuke.menu("Nuke")
menu = toolbar.addMenu("VFX Tools")
menu.addCommand(f"{TOOL_NAME}", f"{TOOL_ENTRY}.launch()")
