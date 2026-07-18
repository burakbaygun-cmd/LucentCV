@echo off
echo Starting LucentCV 2.0 Development Stack...
echo.

:: Explicitly add Node.js to PATH to bypass restart requirement
set PATH=%PATH%;C:\Program Files\nodejs

echo Starting FastAPI Backend in a new window...
start "LucentCV Backend" cmd /k "cd /d %~dp0backend && venv\Scripts\activate && uvicorn main:app --reload --port 8000"

echo Starting Next.js Frontend in a new window...
start "LucentCV Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo LucentCV 2.0 is launching!
echo Backend will be available at http://localhost:8000
echo Frontend will be available at http://localhost:3000
echo.
pause
