<#
Setup script for Gomoku AI (PowerShell)

Usage:
  .\scripts\setup.ps1          # create venv if missing and install deps
  .\scripts\setup.ps1 -Recreate # delete existing .venv and recreate

Requires: Python 3.11 available via the py launcher (py -3.11)
#>

param(
    [switch]$Recreate
)

function Abort([string]$msg){
    Write-Host "ERROR: $msg" -ForegroundColor Red
    exit 1
}

Write-Host "== Gomoku AI setup script =="

# Check for py launcher Python 3.11
Write-Host "Checking for Python 3.11..."
$py = & py -3.11 --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "py -3.11 not found. Please install Python 3.11 and ensure 'py' launcher recognizes it." -ForegroundColor Yellow
    Write-Host "Download: https://www.python.org/downloads/release/python-311/"
    Abort "Python 3.11 required"
}
else {
    Write-Host $py
}

$venvPath = Join-Path -Path (Get-Location) -ChildPath '.venv'

if ($Recreate -and (Test-Path $venvPath)){
    Write-Host "Removing existing .venv..."
    Remove-Item -Recurse -Force $venvPath
}

if (-not (Test-Path $venvPath)){
    Write-Host "Creating virtual environment (.venv) using Python 3.11..."
    & py -3.11 -m venv .venv
    if ($LASTEXITCODE -ne 0) { Abort 'Failed to create virtual environment' }
}
else {
    Write-Host ".venv already exists - skipping creation. Use -Recreate to force recreate." -ForegroundColor Cyan
}

$python = Join-Path $venvPath 'Scripts\python.exe'
Write-Host "Resolved venv python:" $python
if ([string]::IsNullOrWhiteSpace($python) -or -not (Test-Path -Path $python)) { Abort "Python executable not found in .venv ($python)" }

Write-Host "Upgrading pip, setuptools and wheel..."
& "$python" -m pip install --upgrade pip setuptools wheel
if ($LASTEXITCODE -ne 0) { Abort 'Failed to upgrade packaging tools' }

if (Test-Path 'requirements.txt'){
    Write-Host "Installing requirements from requirements.txt..."
    & "$python" -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "requirements installation failed. Trying to install pygame fallback..." -ForegroundColor Yellow
        & "$python" -m pip install pygame==2.1.3
        if ($LASTEXITCODE -ne 0) { Abort 'Failed to install pygame' }
    }
}
else {
    Write-Host "No requirements.txt found - installing pygame as minimum dependency"
    & "$python" -m pip install pygame==2.1.3
    if ($LASTEXITCODE -ne 0) { Abort 'Failed to install pygame' }
}

Write-Host "Setup complete. To run the app:"
Write-Host "  .\\.venv\\Scripts\\Activate.ps1" -ForegroundColor Green
Write-Host "  python src/main.py" -ForegroundColor Green

Write-Host "If you want this script to recreate the venv, run: .\\scripts\\setup.ps1 -Recreate" -ForegroundColor Cyan
