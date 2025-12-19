$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Write-Host "Launching Jupyter Notebook in: $scriptDir"
Set-Location $scriptDir
python -m notebook
