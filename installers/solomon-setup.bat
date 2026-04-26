@echo off
setlocal EnableDelayedExpansion

:: ============================================================
:: Solomon OS - One-Click Windows Installer
:: Double-click this file and Solomon OS installs itself
:: ============================================================

set "REPO_URL=https://github.com/jvanleur2234-glitch/zo-restore"

echo.
echo  #############################################
echo  #       Solomon OS - One-Click Install      #
echo  #############################################
echo.

:: Check if WSL is installed
wsl --status >nul 2>&1
if errorlevel 1 (
    echo WSL not found. Installing Windows Subsystem for Linux...
    wsl --install -d Ubuntu
    echo.
    echo  #############################################
    echo  #  WSL installation requires a COMPUTER RESTART #
    echo  #  Please RESTART your PC, then run again.  #
    echo  #############################################
    echo.
    pause
    exit /b 1
)

:: Check if already installed
wsl -d Ubuntu -- bash -c "test -f ~/solomon-os/solomon" 2>nul
if not errorlevel 1 (
    echo [OK] Solomon OS is already installed.
    goto :LAUNCH
)

:: Clone and install
echo [1/2] Downloading Solomon OS...
wsl -d Ubuntu -- bash -c " ^
mkdir -p ~/solomon-os 2>/dev/null; ^
cd ~/solomon-os; ^
echo 'Cloning from GitHub...'; ^
git clone --depth 1 %REPO_URL% . 2>/dev/null || echo 'Repo already exists, skipping clone'; ^
echo 'Running installer...'; ^
bash files/install.sh; ^
echo 'Installation complete!'; ^
" 2>nul

:: Start heartbeat
echo [2/2] Starting Solomon OS in background...
wsl -d Ubuntu -- bash -c "cd ~/solomon-os && nohup bash .agent/heartbeat/run_heartbeat.sh > /dev/null 2>&1 &" 2>nul

echo.
echo  #############################################
echo  #           Installation Complete!           #
echo  #############################################
echo.
echo To check Solomon OS, open Ubuntu and run:
echo   cd ^~/solomon-os ^&^& ./solomon status
echo.

:LAUNCH
start wsl
pause
