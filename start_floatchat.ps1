# FloatChat PowerShell Startup Script
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "         FloatChat - React Only System        " -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Set location
Set-Location "C:\Users\yashw\FLOATCHAT"

# Add Node.js to PATH
$env:PATH += ";C:\Program Files\nodejs"

# Check Node.js
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js required. Install from: https://nodejs.org/" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Starting FloatChat React System..." -ForegroundColor Green
Write-Host ""

# Start Backend
Write-Host "🔗 Starting Backend API..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\yashw\FLOATCHAT'; python start_backend.py"

Start-Sleep 3

# Start React Frontend
Write-Host "⚛️ Starting React Frontend..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\yashw\FLOATCHAT\frontend'; `$env:PATH += ';C:\Program Files\nodejs'; npm run dev"

Write-Host ""
Write-Host "🌐 Access: http://localhost:5173" -ForegroundColor Magenta
Write-Host "🔧 API: http://127.0.0.1:8001" -ForegroundColor Magenta
Write-Host ""
Write-Host "✅ FloatChat React system is starting..." -ForegroundColor Green
Read-Host "Press Enter to exit"
