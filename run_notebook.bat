@echo off
SET "SCRIPT_DIR=%~dp0"
echo Launching Jupyter Notebook in: "%SCRIPT_DIR%"
cd /d "%SCRIPT_DIR%"
python -m notebook
