"""
Simple FloatChat Launcher
=========================
A simplified script to start the FloatChat system.
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def start_backend():
    """Start the backend server in a separate process"""
    print("🚀 Starting backend server...")

    # Change to the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)

    # Start backend in a new console window
    backend_cmd = [
        sys.executable,
        "backend_mock.py"
    ]

    if os.name == 'nt':  # Windows
        # Start in new command window
        subprocess.Popen(
            ['cmd', '/c', 'start', 'cmd', '/k'] + backend_cmd,
            cwd=project_dir
        )
    else:  # Unix/Linux/Mac
        subprocess.Popen(
            ['gnome-terminal', '--', 'python'] + backend_cmd[1:],
            cwd=project_dir
        )

    print("✅ Backend starting in separate window...")
    return True

def start_frontend():
    """Start the frontend in a separate process"""
    print("🎨 Starting frontend...")

    project_dir = Path(__file__).parent

    # Start frontend in a new console window
    frontend_cmd = [
        sys.executable,
        "-m", "streamlit", "run", "streamlit_app.py",
        "--server.headless", "false"
    ]

    if os.name == 'nt':  # Windows
        subprocess.Popen(
            ['cmd', '/c', 'start', 'cmd', '/k'] + frontend_cmd,
            cwd=project_dir
        )
    else:  # Unix/Linux/Mac
        subprocess.Popen(
            ['gnome-terminal', '--'] + frontend_cmd,
            cwd=project_dir
        )

    print("✅ Frontend starting in separate window...")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import streamlit
        import plotly
        import pandas
        print("✅ All dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def wait_for_services():
    """Wait for services to start and open browser"""
    print("\n⏳ Waiting for services to start...")

    # Wait a bit for services to start
    for i in range(10, 0, -1):
        print(f"Opening browser in {i} seconds...", end='\r')
        time.sleep(1)

    print("\n🌐 Opening FloatChat in browser...")

    # Try to open the frontend URL
    try:
        webbrowser.open("http://localhost:8501")
        print("✅ Browser opened to http://localhost:8501")
    except Exception as e:
        print(f"⚠️  Could not open browser: {e}")
        print("Please manually open: http://localhost:8501")

def main():
    """Main function"""
    print("🌊 FloatChat Simple Launcher")
    print("=" * 40)

    # Check dependencies
    if not check_dependencies():
        input("Press Enter to exit...")
        return

    # Start services
    try:
        if start_backend():
            time.sleep(2)  # Give backend time to start

        if start_frontend():
            wait_for_services()

        print("\n" + "=" * 40)
        print("🎉 FloatChat is starting up!")
        print("📊 Frontend: http://localhost:8501")
        print("🔧 Backend API: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print("\n💡 Try asking: 'Show me temperature profiles near the equator'")
        print("\n⚠️  Close this window to stop the services")

    except Exception as e:
        print(f"❌ Error starting services: {e}")

    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main()
