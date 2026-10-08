@echo off
setlocal
cd /d "%~dp0frontend"

where node >nul 2>nul
if errorlevel 1 (
  echo Node.js was not found. Install the LTS version from nodejs.org.
  pause & exit /b 1
)

if not exist node_modules (
  echo Installing packages (first time takes a few minutes)...
  call npm install
)

echo.
echo Frontend starting. Open http://localhost:5173   (keep this window open)
call npm run dev
pause
