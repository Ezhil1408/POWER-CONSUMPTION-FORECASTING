#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "Launching Jupyter Notebook in: \"$SCRIPT_DIR\""
cd "$SCRIPT_DIR"
python3 -m notebook || python -m notebook
