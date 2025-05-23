import os
import sys
import subprocess
import nuke

# Setup tool
TOOL_NAME = "Review Export Tool"
FOLDER_NAME = "review_export_tool"
GITHUB_URL = f"https://github.com/Chilanguiux/nuke_tools.git"
TOOL_DIR = os.path.expanduser(f"~/.nuke/tools/{TOOL_NAME}")
TOOL_ENTRY = "tool"

def update_tool_repo(repo_dir):
    try:
        if os.path.exists(GITHUB_URL):
            os.chdir(repo_dir)
            subprocess.run(["git", "fetch"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            status = subprocess.check_output(["git", "status"]).decode("utf-8")
            if "behind" in status:
                print(f"Updating repo at {repo_dir}")
                subprocess.run(["git", "pull"], check=True)
            else:
                print("Repo is already up-to-date.")
        else:
            print("No .git folder found. Not a valid repo.")
    except Exception as e:
        nuke.message(f"Error updating tool repo:\n{e}")

# Clone repo if exists
if not os.path.exists(TOOL_DIR):
    nuke.message(f"{TOOL_NAME} not found. Cloning from GitHub...")
    try:
        subprocess.run(["git", "clone", GITHUB_URL, TOOL_DIR], check=True)
    except Exception as e:
        nuke.message(f"Error cloning tool: {e}")
else:
    print(f"{TOOL_NAME} already exists in: {TOOL_DIR}")
    update_tool_repo(TOOL_DIR)

# Adding to sys.path
if TOOL_DIR not in sys.path:
    sys.path.append(os.path.join(TOOL_DIR, FOLDER_NAME))

# Importing tool
try:
    import tool  
    import importlib
    tool_module = importlib.import_module(TOOL_ENTRY)
except Exception as e:
    nuke.message(f"Error loading tool module: {e}")

# Nuke menu setup
toolbar = nuke.menu("Nuke")
menu = toolbar.addMenu("VFX Tools")
menu.addCommand(f"{TOOL_NAME}", f"{TOOL_ENTRY}.launch()")
