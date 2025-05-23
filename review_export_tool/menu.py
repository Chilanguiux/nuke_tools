import os
import subprocess
import sys
import nuke

GITHUB_URL = f"https://github.com/Chilanguiux/nuke_tools.git"
BASE_DIR = os.path.expanduser("~/.nuke/tools")
TOOLS_MODULE = "tools"

sys.path.append(BASE_DIR)


def is_git_repo(path):
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return result.stdout.strip() == "true"
    except Exception:
        return False

def update_repo(path, name):
    """Updates a Git repository if not updated."""
    try:
        subprocess.run(["git", "fetch"], cwd=path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        status = subprocess.check_output(
            ["git", "rev-list", "--count", "--left-right", "@{u}...HEAD"],
            cwd=path
        ).decode().strip()

        behind = int(status.split()[0]) if status else 0
        if behind > 0:
            nuke.tprint(f"Repo '{name}' outdated, running a pull request...")
            subprocess.run(["git", "pull"], cwd=path, check=True)
        else:
            nuke.tprint(f"Repo '{name}' is updated.")
    except Exception as e:
        nuke.tprint(f"Error updating repo '{name}': {e}")

def setup_tools():
    """Checks each repo folder and added it to the sys.path."""
    if not os.path.exists(BASE_DIR):
        clone_base_repo()

    for name in os.listdir(BASE_DIR):
        repo_path = os.path.join(BASE_DIR, name)
        if "__pycache__" in repo_path:
            continue
        if not os.path.isdir(repo_path):
            continue
        if not is_git_repo(repo_path):
            continue

        update_repo(repo_path, name)

        if repo_path not in sys.path:
            sys.path.append(repo_path)
            
def clone_base_repo():
    """Clones the main repo if missed."""
    try:
        nuke.tprint(f"Cloning repo from: {GITHUB_URL}")
        subprocess.run(["git", "clone", GITHUB_URL, BASE_DIR], check=True)
    except Exception as e:
        nuke.message(f"Error cloning the repo:\n{e}")

def add_tools_to_nuke_menu():
    """Adds the Nuke menu for each tool."""
    try:
        import tools

        toolbar = nuke.menu("Nuke")
        menu = toolbar.addMenu("VFX Tools")

        menu.addCommand("Review Export Tool", "import tools; tools.launch_export_tool()")
        menu.addCommand("Node Cleaner Tool", "import tools; tools.launch_cleaner_tool()")

        nuke.tprint("Tools properly loaded in VFX Tools menu.")

    except ImportError as e:
        nuke.message(f"Error importing 'tools.py':\n{e}")
    except Exception as e:
        nuke.message(f"Error while loading Nuke menu:\n{e}")

# main process
setup_tools()
add_tools_to_nuke_menu()
