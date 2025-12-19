@echo off
REM Locate script directory (handles spaces)
SET "SCRIPT_DIR=%~dp0"
echo Installing requirements from: "%SCRIPT_DIR%requirements.txt"
python -m pip install --upgrade pip
python -m pip install -r "%SCRIPT_DIR%requirements.txt"
echo Install complete.
pause >nul
