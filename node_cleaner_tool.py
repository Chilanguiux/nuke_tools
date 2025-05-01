# Nuke Cleaner Node Tool
 
import nuke
import os
def full_clean():
    def backup_script():
        current_script = nuke.root().name()
        if current_script == "Root":
            return None
        path, name = os.path.split(current_script)
        backup_name = name.replace(".nk", "_backup.nk")
        backup_path = os.path.join(path, backup_name)
        nuke.scriptSaveAs(backup_path)
        return backup_path
    def delete_unused_nodes():
        deleted = 0
        for node in nuke.allNodes(recurseGroups=True):
            if node.Class() == "Root":
                continue
            if not node.dependent(nuke.INPUTS) and not node.dependencies():
                nuke.delete(node)
                deleted += 1
        return deleted
    def delete_unconnected_dots():
        deleted = 0
        for node in nuke.allNodes("Dot"):
            if not node.dependent(nuke.INPUTS) and not node.dependencies():
                nuke.delete(node)
                deleted += 1
        return deleted
    def arrange_nodes_horizontally(start_x=0, start_y=0, spacing=150):
        nodes = [n for n in nuke.allNodes() if n.Class() != "Root"]
        for i, node in enumerate(nodes):
            node.setXpos(start_x + i * spacing)
            node.setYpos(start_y)
    backup_path = backup_script()
    deleted = delete_unused_nodes()
    dots_deleted = delete_unconnected_dots()
    arrange_nodes_horizontally()
    msg = f"Complete:\n"
    if backup_path:
        msg += f"Backup created: {backup_path}\n"
    msg += f"cleaned nodes: {deleted}\n"
    msg += f"Dots nodes removed: {dots_deleted}\n"
    msg += f"Nodes fixes=d horizontally."
    nuke.message(msg)
# Add the new menu
menu = nuke.menu("Nuke")
tools_menu = menu.addMenu("My Menu")
tools_menu.addCommand("Node cleaner tool", full_clean)
