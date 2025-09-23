#!/usr/bin/env python3
"""
FloatChat Integrated Frontend Manager
====================================
This script manages both Streamlit and React/Vite frontends,
providing a seamless integrated experience.
"""

import os
import sys
import time
import subprocess
import threading
import webbrowser
from pathlib import Path

class IntegratedFrontendManager:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.frontend_path = self.base_path / "frontend"
        self.venv_path = self.base_path / ".venv"
        self.processes = []

    def setup_node_dependencies(self):
        """Install Node.js dependencies for React/Vite frontend"""
        print("🔧 Setting up Node.js dependencies...")

        os.chdir(self.frontend_path)

        # Check if node_modules exists
        if not (self.frontend_path / "node_modules").exists():
            print("📦 Installing npm dependencies...")
            result = subprocess.run(["npm", "install"], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Failed to install npm dependencies: {result.stderr}")
                return False

        print("✅ Node.js dependencies ready")
        return True

    def start_backend(self):
        """Start the FastAPI backend server"""
        print("🚀 Starting FastAPI Backend...")

        backend_cmd = [
            str(self.venv_path / "Scripts" / "python.exe"),
            "start_backend.py"
        ]

        try:
            process = subprocess.Popen(
                backend_cmd,
                cwd=self.base_path,
                creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
            )
            self.processes.append(("Backend", process))
            print("✅ Backend server starting on http://127.0.0.1:8001")
            return True
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False

    def start_streamlit(self):
        """Start the Streamlit frontend"""
        print("🎨 Starting Streamlit Frontend...")

        streamlit_cmd = [
            str(self.venv_path / "Scripts" / "streamlit"),
            "run",
            "streamlit_app.py",
            "--server.port=8502",
            "--server.headless=true"
        ]

        try:
            process = subprocess.Popen(
                streamlit_cmd,
                cwd=self.base_path,
                creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
            )
            self.processes.append(("Streamlit", process))
            print("✅ Streamlit frontend starting on http://localhost:8502")
            return True
        except Exception as e:
            print(f"❌ Failed to start Streamlit: {e}")
            return False

    def start_react(self):
        """Start the React/Vite frontend"""
        print("⚛️ Starting React/Vite Frontend...")

        os.chdir(self.frontend_path)

        try:
            process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=self.frontend_path,
                creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
            )
            self.processes.append(("React/Vite", process))
            print("✅ React frontend starting on http://localhost:5173")
            return True
        except Exception as e:
            print(f"❌ Failed to start React frontend: {e}")
            return False

    def wait_for_services(self):
        """Wait for all services to be ready"""
        print("⏳ Waiting for services to initialize...")
        time.sleep(8)  # Give services time to start

        # Check if services are responding
        import requests

        services = [
            ("Backend API", "http://127.0.0.1:8001"),
            ("Streamlit UI", "http://localhost:8502"),
            ("React UI", "http://localhost:5173")
        ]

        for name, url in services:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ {name} is ready")
                else:
                    print(f"⚠️ {name} responded with status {response.status_code}")
            except:
                print(f"⚠️ {name} is not responding yet (may still be starting)")

    def open_browsers(self):
        """Open browsers for both frontends"""
        print("🌐 Opening web interfaces...")

        time.sleep(2)

        # Open Streamlit (main interface)
        webbrowser.open("http://localhost:8502")

        time.sleep(1)

        # Open React (modern interface)
        webbrowser.open("http://localhost:5173")

    def start_integrated_system(self):
        """Start the complete integrated system"""
        print("🌊 FloatChat Integrated Frontend Manager")
        print("=" * 50)

        # Setup dependencies
        if not self.setup_node_dependencies():
            return False

        # Start all services
        services_started = 0

        if self.start_backend():
            services_started += 1

        if self.start_streamlit():
            services_started += 1

        if self.start_react():
            services_started += 1

        if services_started == 3:
            print(f"✅ All {services_started} services started successfully!")

            # Wait for services to be ready
            self.wait_for_services()

            # Open browsers
            self.open_browsers()

            print("\\n🎉 FloatChat Integrated System is running!")
            print("=" * 50)
            print("🔗 Access Points:")
            print("   • Streamlit UI (Production): http://localhost:8502")
            print("   • React UI (Modern):        http://localhost:5173")
            print("   • Backend API:              http://127.0.0.1:8001")
            print("\\n📱 Features Available:")
            print("   • AI-powered chat interface")
            print("   • Interactive ocean maps")
            print("   • Real-time data visualization")
            print("   • ARGO float monitoring")
            print("\\n💡 Usage:")
            print("   • Use Streamlit for data analysis and chat")
            print("   • Use React for modern UI and advanced features")
            print("   • Both interfaces share the same backend data")
            print("\\n⏹️ Press Ctrl+C to stop all services")

            # Keep the script running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.cleanup()
        else:
            print(f"❌ Only {services_started}/3 services started. Check errors above.")
            self.cleanup()
            return False

    def cleanup(self):
        """Clean up all processes"""
        print("\\n🧹 Stopping all services...")

        for name, process in self.processes:
            try:
                process.terminate()
                print(f"⏹️ Stopped {name}")
            except:
                pass

        print("✅ All services stopped")

if __name__ == "__main__":
    manager = IntegratedFrontendManager()
    manager.start_integrated_system()
