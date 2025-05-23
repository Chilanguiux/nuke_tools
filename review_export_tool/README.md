# Auto Review Export Tool for Nuke _Non-Commercial_

**A Nuke tool designed to help students and new compositors set up a basic review comp quickly and professionally.**

## Purpose

This tool was created with **students learning Nuke** in mind. It simplifies the process of generating a quickTime ".mov" with:

- A customizable **slate** (solid or image)
- **Burn-in text** (shot name, frame)
- An optional **logo** positioned top-right
- Merged slate + footage
- Final output using libx264 codec (compatible with most review pipelines)

## Features

- Works in **Nuke Non-Commercial** (within node limits)
- Minimal and intuitive **PySide UI**
- File pickers for **output path**, **logo**, and **slate background**
- Automatically formats and scales the logo
- Great for **school reviews**, **assignments**, or **learning real comp workflows**

# Installation (Automatic)

1. Copy "menu.py" into your local "~/.nuke/" folder.
2. Launch Nuke.
3. The tool will appear under "VFX Tools > Review Export Tool > Launch".

No manual installation or setup needed. The tool auto-installs from GitHub the first time.

# Usage

Select or create a Read node with your shot

Open the Auto Review Export tool

# Choose

Output .mov path

Optional slate background (solid or image)

Optional logo

**Click Create Export**

The tool builds the comp, adds burn-ins, merges elements, and writes a .mov

# Why This Tool?

Nuke has a learning curve, especially when preparing shots for dailies or reviews.

# Compatibility

- Nuke Non-Commercial (tested on Nuke 13–16)
- Windows/macOS/Linux
- PySide2 and PySide6 fallback

# Credits

Created by **Erik E.**, inspired by real production review workflows and adapted for learning environments.
