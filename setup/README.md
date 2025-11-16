# Quick Start — Python Setup

- Learn basics: open the example scripts (coffee_store_basic.py and coffee_store_advanced.py) to see simple Python constructs (print, input, lists, dicts, loops, functions) if you are new to Python.

- Test your Python environment:
  - Run: `python hello.py`
  - If it prints the hello message, your Python env is working.

- Install openai (do this at home via OPS VPN before Workshop #1):
  - Upgrade installers and install:
    - `python -m pip install --upgrade pip setuptools wheel`
    - `python -m pip install openai`
  - Verify: `python check_openai.py

- Configure VS Code for shared functionality:
  - Create a `.vscode` folder at the root of the bootcamp project (if it doesn't exist): `mkdir .vscode`
  - Copy `launch.json` and `settings.json` into the `.vscode` folder from the shared configuration
  - These files enable common debugging and editor settings across all subfolders (test/, assignments/, etc.)
  - Restart VS Code to apply the settings


Note: Your org network may block installs. If you cannot install while on your org network, connect from home via the org VPN.

