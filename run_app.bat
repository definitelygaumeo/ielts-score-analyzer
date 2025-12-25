@echo off
title IELTS Score Analyzer
echo ============================================
echo   IELTS Score Analyzer - Starting...
echo ============================================
echo.

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if PyQt6 is installed
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing PyQt6...
    pip install PyQt6
)

echo [INFO] Starting application...
echo.

python ielts_analyzer_app.py

if errorlevel 1 (
    echo.
    echo [ERROR] Application crashed. Press any key to exit.
    pause
)

