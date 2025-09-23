# Node.js Setup Guide for FloatChat Frontend

## 🚨 Current Issue
The React/Vite frontend requires Node.js to be properly installed and configured on Windows.

## 📥 Installing Node.js

### Method 1: Official Installer (Recommended)
1. **Download Node.js**: Go to https://nodejs.org/
2. **Choose LTS Version**: Download the "LTS" (Long Term Support) version
3. **Run Installer**:
   - Choose "Add to PATH" option ✅
   - Install for all users ✅
   - Install npm package manager ✅
4. **Restart Computer**: This ensures PATH is updated
5. **Verify Installation**:
   ```bash
   # Open new PowerShell and test:
   node --version    # Should show v18.x.x or v20.x.x
   npm --version     # Should show 9.x.x or 10.x.x
   ```

### Method 2: Chocolatey (Advanced Users)
```powershell
# Run PowerShell as Administrator
choco install nodejs
```

### Method 3: Winget (Windows 11)
```powershell
winget install OpenJS.NodeJS
```

## 🔧 After Node.js Installation

### 1. Restart Your Computer
This is **critical** to ensure the PATH environment variable is updated.

### 2. Test Installation
```powershell
# Open new PowerShell window
node --version
npm --version
npx --version
```

### 3. Install Frontend Dependencies
```powershell
cd "C:\Users\yashw\FLOATCHAT\frontend"
npm install
```

### 4. Test React Frontend
```powershell
cd "C:\Users\yashw\FLOATCHAT\frontend"
npm run dev
```

## 🛠️ Alternative Solutions

### Option A: Use Only Streamlit (Simpler)
If Node.js installation is problematic, you can use just the Streamlit frontend:

```bash
# Start only backend + Streamlit
start_floatchat_clean.bat
```

This gives you:
- ✅ AI chat interface
- ✅ Interactive maps
- ✅ Data visualization
- ✅ All core functionality

### Option B: Docker Approach (Advanced)
```dockerfile
# Create Dockerfile for React frontend
FROM node:18-alpine
WORKDIR /app
COPY frontend/ .
RUN npm install
CMD ["npm", "run", "dev"]
```

### Option C: Use Online IDEs
- **CodeSandbox**: Import the frontend folder
- **StackBlitz**: Works with Vite projects
- **Gitpod**: Full development environment

## 🎯 Quick Fixes

### Fix 1: PATH Issues
```powershell
# Check if Node.js is in PATH
$env:PATH -split ';' | Select-String "node"

# If not found, add manually:
# Go to System Properties > Environment Variables
# Add: C:\Program Files\nodejs (or installation path)
```

### Fix 2: npm Issues
```powershell
# Clear npm cache
npm cache clean --force

# Use different registry if needed
npm config set registry https://registry.npmjs.org/
```

### Fix 3: Permission Issues
```powershell
# Run PowerShell as Administrator
npm config set prefix C:\Users\%USERNAME%\AppData\Roaming\npm
```

## ✅ Verification Checklist

Before running the integrated system:

- [ ] Node.js installed (v16+ recommended)
- [ ] npm working (`npm --version`)
- [ ] Can run `npm install` in frontend folder
- [ ] No error when running `npm run dev`
- [ ] Backend is running on port 8001
- [ ] Streamlit is working independently

## 🚀 Once Node.js is Working

Run the complete system:
```bash
# Full integration with both frontends
start_complete_system.bat
```

Access points:
- **React UI**: http://localhost:5173
- **Streamlit UI**: http://localhost:8502
- **Backend API**: http://127.0.0.1:8001

## 💡 Pro Tips

1. **Always restart** after Node.js installation
2. **Use LTS version** for stability
3. **Check PATH** if commands not found
4. **Streamlit works independently** if React has issues
5. **Both frontends** share the same backend data

---

**Need help? The Streamlit frontend provides all core functionality while you set up Node.js! 🌊**
