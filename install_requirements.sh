#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "Installing requirements from: \"$SCRIPT_DIR/requirements.txt\""
python3 -m pip install --upgrade pip 2>/dev/null || python -m pip install --upgrade pip
python3 -m pip install -r "$SCRIPT_DIR/requirements.txt" 2>/dev/null || python -m pip install -r "$SCRIPT_DIR/requirements.txt"
echo "Install complete."