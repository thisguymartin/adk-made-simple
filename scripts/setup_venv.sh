#!/usr/bin/env zsh
# Setup Python venv and install dependencies

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "[INFO] Python venv created and dependencies installed. To activate: source .venv/bin/activate"
