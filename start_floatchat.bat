@echo off
echo ===============================================
echo         FloatChat - React Only System
echo ===============================================
echo.

cd /d "C:\Users\yashw\FLOATCHAT"

REM Add Node.js to PATH for this session
set "PATH=%PATH%;C:\Program Files\nodejs"

REM Check Node.js
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js required. Install from: https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Starting FloatChat React System...
echo.

REM Start Backend
echo 🔗 Starting Backend API...
start "FloatChat Backend" cmd /k "cd /d C:\Users\yashw\FLOATCHAT && C:\Users\yashw\FLOATCHAT\.venv\Scripts\python.exe start_backend.py"

timeout /t 3 /nobreak > nul

REM Start React Frontend
echo ⚛️ Starting React Frontend...
start "FloatChat React" cmd /k "cd /d C:\Users\yashw\FLOATCHAT\frontend && npm run dev"

echo.
echo 🌐 Access: http://localhost:5173
echo 🔧 API: http://127.0.0.1:8001
echo.
echo ✅ FloatChat React system is starting...
pause > nul
