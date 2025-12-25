@echo off
title Building IELTS Analyzer Executable
echo ============================================
echo   Building Windows Executable (.exe)
echo ============================================
echo.

cd /d "%~dp0"

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing PyInstaller...
    pip install pyinstaller
)

echo [INFO] Building executable...
echo This may take a few minutes...
echo.

pyinstaller --onefile ^
    --windowed ^
    --name "IELTS_Analyzer" ^
    --icon "icon.ico" ^
    --add-data "templates;templates" ^
    ielts_analyzer_app.py

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Build Complete!
echo ============================================
echo.
echo Executable file: dist\IELTS_Analyzer.exe
echo.
pause

