$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Write-Host "Installing requirements from: $scriptDir\requirements.txt"
python -m pip install --upgrade pip
python -m pip install -r "$scriptDir\requirements.txt"
Write-Host "Install complete."
