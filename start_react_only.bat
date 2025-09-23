@echo off
echo ===============================================
echo     FloatChat React Frontend Only
echo ===============================================
echo.

cd /d "C:\Users\yashw\FLOATCHAT\frontend"

REM Check if Node.js is available
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js is not installed
    echo.
    echo Please install Node.js from: https://nodejs.org/
    echo Or use start_complete_system.bat for Streamlit-only mode
    pause
    exit /b 1
)

REM Check if dependencies are installed
if not exist "node_modules" (
    echo 📦 Installing dependencies...
    npm install
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

echo ✅ Starting React frontend...
echo.
echo Make sure the backend is running on http://127.0.0.1:8001
echo.

npm run dev

pause
