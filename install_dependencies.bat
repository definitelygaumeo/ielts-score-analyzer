@echo off
title Installing IELTS Analyzer Dependencies
echo ============================================
echo   IELTS Score Analyzer - Cai Dat Thu Vien
echo ============================================
echo.

cd /d "%~dp0"

echo [1/5] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [2/5] Installing PyQt6 (GUI)...
pip install PyQt6==6.6.1

echo.
echo [3/5] Installing AI libraries...
echo   - OpenAI (GPT-4)
pip install openai==1.6.1
echo   - Anthropic (Claude)
pip install anthropic==0.8.1
echo   - Google GenAI (Gemini) - NEW PACKAGE
pip install google-genai

echo.
echo [4/5] Installing utilities...
pip install python-dotenv==1.0.0

echo.
echo [5/5] Installing Flask (web version - optional)...
pip install flask==3.0.0 flask-cors==4.0.0

echo.
echo ============================================
echo   Cai Dat Hoan Tat! / Installation Complete!
echo ============================================
echo.
echo Cac thu vien da cai dat:
echo   - PyQt6 (Giao dien)
echo   - OpenAI (GPT-4)
echo   - Anthropic (Claude)
echo   - Google GenAI (Gemini)
echo   - Flask (Web version)
echo.
echo Chay 'run_app.bat' de khoi dong ung dung.
echo.
pause
