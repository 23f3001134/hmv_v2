@echo off
setlocal
cd /d "%~dp0backend"

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.11+ from python.org and tick "Add to PATH".
  pause & exit /b 1
)

if not exist venv (
  echo Creating virtual environment...
  python -m venv venv
)
call venv\Scripts\activate

echo Installing packages (first time takes a minute)...
pip install -q -r requirements.txt
if errorlevel 1 ( echo Package install failed. & pause & exit /b 1 )

python make_env.py
flask --app app init-db
flask --app app seed-admin

echo.
echo Backend starting at http://127.0.0.1:5000   (keep this window open)
python app.py
pause
