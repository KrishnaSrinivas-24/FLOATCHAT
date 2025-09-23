@echo off
echo ===============================================
echo    Node.js Installation Verification
echo ===============================================
echo.

echo Testing Node.js installation...
echo.

REM Test Node.js
echo Checking Node.js version:
node --version
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js not found
    echo.
    echo Please ensure:
    echo   1. Node.js is installed from https://nodejs.org/
    echo   2. You restarted your computer after installation
    echo   3. "Add to PATH" was checked during installation
    echo.
    pause
    exit /b 1
)

REM Test npm
echo.
echo Checking npm version:
npm --version
if %ERRORLEVEL% NEQ 0 (
    echo ❌ npm not found
    pause
    exit /b 1
)

echo.
echo ✅ Node.js and npm are working correctly!
echo.
echo Node.js version:
node --version
echo npm version:
npm --version
echo.

echo Now installing React frontend dependencies...
echo.

cd "C:\Users\yashw\FLOATCHAT\frontend"

if not exist "package.json" (
    echo ❌ Frontend package.json not found
    echo Make sure you're in the correct directory
    pause
    exit /b 1
)

echo Installing dependencies...
npm install

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to install dependencies
    echo.
    echo Trying with legacy peer deps...
    npm install --legacy-peer-deps

    if %ERRORLEVEL% NEQ 0 (
        echo ❌ Still failed. Trying to fix...
        npm cache clean --force
        npm install --legacy-peer-deps --no-optional
    )
)

echo.
echo ✅ Dependencies installed successfully!
echo.
echo Testing React development server...
echo.
echo Starting Vite dev server (press Ctrl+C to stop)...
npm run dev

pause
