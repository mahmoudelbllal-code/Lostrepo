@echo off
echo ========================================
echo Lost & Found AI Backend Setup
echo ========================================
echo.

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
echo (This may take a few minutes on first run - CLIP model ~350MB)
echo.
pip install -r requirements.txt

echo.
echo ========================================
echo Installation complete!
echo Starting Flask server...
echo ========================================
echo.

REM Run the app
python app.py

pause
