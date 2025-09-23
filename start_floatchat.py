"""
FloatChat System Startup Script
===============================
This script helps you start the complete FloatChat system with all components.
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

class FloatChatManager:
    def __init__(self):
        self.processes = []
        self.base_dir = Path(__file__).parent

    def check_prerequisites(self):
        """Check if all prerequisites are installed"""
        print("🔍 Checking prerequisites...")

        # Check Python environment
        try:
            import fastapi, streamlit, plotly, pandas
            print("✅ Python dependencies installed")
        except ImportError as e:
            print(f"❌ Missing Python dependencies: {e}")
            print("Run: pip install -r requirements.txt")
            return False

        # Check if backend files exist
        required_files = [
            "backend_mock.py",
            "streamlit_app.py",
            "requirements.txt"
        ]

        for file in required_files:
            if not (self.base_dir / file).exists():
                print(f"❌ Missing required file: {file}")
                return False

        print("✅ All prerequisites met")
        return True

    def start_backend(self, mock_mode=True):
        """Start the backend server"""
        print("🚀 Starting backend server...")

        backend_file = "backend_mock.py" if mock_mode else "backend_server.py"

        cmd = [
            sys.executable,
            str(self.base_dir / backend_file)
        ]

        process = subprocess.Popen(
            cmd,
            cwd=str(self.base_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

        self.processes.append(("Backend", process))

        # Wait a bit for the server to start
        time.sleep(3)

        if process.poll() is None:
            print("✅ Backend server started")
            return True
        else:
            print("❌ Backend server failed to start")
            return False

    def start_frontend(self):
        """Start the Streamlit frontend"""
        print("🎨 Starting Streamlit frontend...")

        cmd = [
            sys.executable,
            "-m", "streamlit", "run",
            str(self.base_dir / "streamlit_app.py"),
            "--server.headless", "true",
            "--server.port", "8501"
        ]

        process = subprocess.Popen(
            cmd,
            cwd=str(self.base_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

        self.processes.append(("Frontend", process))

        # Wait for Streamlit to start
        time.sleep(5)

        if process.poll() is None:
            print("✅ Streamlit frontend started")
            return True
        else:
            print("❌ Streamlit frontend failed to start")
            return False

    def monitor_processes(self):
        """Monitor running processes"""
        def monitor_process(name, process):
            try:
                for line in iter(process.stdout.readline, ''):
                    if line:
                        print(f"[{name}] {line.strip()}")

                process.stdout.close()
                process.wait()
            except Exception as e:
                print(f"❌ Error monitoring {name}: {e}")

        for name, process in self.processes:
            thread = threading.Thread(target=monitor_process, args=(name, process))
            thread.daemon = True
            thread.start()

    def stop_all(self):
        """Stop all processes"""
        print("\n🛑 Stopping all processes...")

        for name, process in self.processes:
            try:
                if process.poll() is None:
                    print(f"Stopping {name}...")
                    process.terminate()

                    # Wait for graceful shutdown
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        print(f"Force killing {name}...")
                        process.kill()
                        process.wait()

                    print(f"✅ {name} stopped")
            except Exception as e:
                print(f"❌ Error stopping {name}: {e}")

        self.processes.clear()

    def show_status(self):
        """Show system status"""
        print("\n📊 System Status:")
        print("=" * 50)

        # Check backend
        try:
            import requests
            response = requests.get("http://localhost:8000", timeout=5)
            if response.status_code == 200:
                print("🟢 Backend: Online (http://localhost:8000)")
                print("📚 API Docs: http://localhost:8000/docs")
            else:
                print("🟡 Backend: Responding but with issues")
        except:
            print("🔴 Backend: Offline")

        # Check frontend
        try:
            import requests
            response = requests.get("http://localhost:8501", timeout=5)
            if response.status_code == 200:
                print("🟢 Frontend: Online (http://localhost:8501)")
            else:
                print("🟡 Frontend: Responding but with issues")
        except:
            print("🔴 Frontend: Offline")

        print("\n📝 Quick Access URLs:")
        print("• FloatChat App: http://localhost:8501")
        print("• Backend API: http://localhost:8000")
        print("• API Documentation: http://localhost:8000/docs")
        print("\n💡 Try asking: 'Show me temperature profiles near the equator'")

    def run(self, mock_mode=True, monitor=True):
        """Run the complete system"""
        print("🌊 FloatChat System Manager")
        print("=" * 50)

        # Setup signal handlers
        def signal_handler(signum, frame):
            print("\n⚡ Received shutdown signal...")
            self.stop_all()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        try:
            # Check prerequisites
            if not self.check_prerequisites():
                return False

            # Start backend
            if not self.start_backend(mock_mode):
                return False

            # Start frontend
            if not self.start_frontend():
                self.stop_all()
                return False

            # Show status
            time.sleep(2)
            self.show_status()

            if monitor:
                print("\n🔍 Monitoring processes... (Press Ctrl+C to stop)")
                self.monitor_processes()

                # Keep the script running
                try:
                    while True:
                        time.sleep(1)
                        # Check if any process died
                        for name, process in self.processes:
                            if process.poll() is not None:
                                print(f"❌ {name} process died")
                                self.stop_all()
                                return False
                except KeyboardInterrupt:
                    pass

            return True

        except Exception as e:
            print(f"❌ Error: {e}")
            self.stop_all()
            return False
        finally:
            self.stop_all()

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="FloatChat System Manager")
    parser.add_argument("--full", action="store_true",
                       help="Use full backend (requires database setup)")
    parser.add_argument("--no-monitor", action="store_true",
                       help="Don't monitor processes (start and exit)")

    args = parser.parse_args()

    manager = FloatChatManager()

    mock_mode = not args.full
    monitor = not args.no_monitor

    if mock_mode:
        print("🧪 Running in MOCK MODE (no database required)")
    else:
        print("🔴 Running in FULL MODE (requires database setup)")

    success = manager.run(mock_mode=mock_mode, monitor=monitor)

    if success:
        print("✅ FloatChat system started successfully!")
    else:
        print("❌ Failed to start FloatChat system")
        sys.exit(1)

if __name__ == "__main__":
    main()
