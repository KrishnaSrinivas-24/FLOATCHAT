#!/usr/bin/env python3
"""
FloatChat Integration Test Suite
===============================
Tests the integration between React frontend, Streamlit frontend, and FastAPI backend
"""

import requests
import time
import json
from pathlib import Path

class IntegrationTester:
    def __init__(self):
        self.backend_url = "http://127.0.0.1:8001"
        self.streamlit_url = "http://localhost:8502"
        self.react_url = "http://localhost:5173"

    def test_backend_health(self):
        """Test if backend is responding"""
        try:
            response = requests.get(f"{self.backend_url}/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print("✅ Backend Health Check:")
                print(f"   Status: {data.get('status', 'Unknown')}")
                print(f"   Mode: {data.get('mode', 'Unknown')}")
                return True
        except Exception as e:
            print(f"❌ Backend Health Check Failed: {e}")
            return False

    def test_backend_endpoints(self):
        """Test key backend API endpoints"""
        endpoints = [
            ("/api/stats", "Database stats"),
            ("/api/floats", "Float data"),
            ("/api/floats?lat_min=0&lat_max=10", "Filtered floats")
        ]

        print("\\n🔗 Testing Backend API Endpoints:")
        all_passed = True

        for endpoint, description in endpoints:
            try:
                response = requests.get(f"{self.backend_url}{endpoint}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ {description}: {len(data) if isinstance(data, list) else 'OK'}")
                else:
                    print(f"   ❌ {description}: HTTP {response.status_code}")
                    all_passed = False
            except Exception as e:
                print(f"   ❌ {description}: {e}")
                all_passed = False

        return all_passed

    def test_chat_endpoint(self):
        """Test AI chat functionality"""
        print("\\n🤖 Testing AI Chat Endpoint:")

        test_message = "Show me temperature data near the equator"
        payload = {
            "message": test_message,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
        }

        try:
            response = requests.post(
                f"{self.backend_url}/api/chat",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Chat Response Generated")
                print(f"   📝 Reply Length: {len(data.get('reply', ''))}")
                print(f"   🎯 Actions: {len(data.get('actions', []))}")
                print(f"   📊 Confidence: {data.get('confidence', 0):.2f}")
                return True
            else:
                print(f"   ❌ Chat API: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Chat API Error: {e}")
            return False

    def test_frontend_accessibility(self):
        """Test if frontends are accessible"""
        frontends = [
            (self.streamlit_url, "Streamlit Frontend"),
            (self.react_url, "React Frontend")
        ]

        print("\\n🌐 Testing Frontend Accessibility:")
        all_accessible = True

        for url, name in frontends:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"   ✅ {name}: Accessible")
                else:
                    print(f"   ❌ {name}: HTTP {response.status_code}")
                    all_accessible = False
            except Exception as e:
                print(f"   ❌ {name}: {e}")
                all_accessible = False

        return all_accessible

    def test_cors_configuration(self):
        """Test CORS configuration for frontend integration"""
        print("\\n🔗 Testing CORS Configuration:")

        # Simulate a frontend request with Origin header
        headers = {
            'Origin': 'http://localhost:5173',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.get(
                f"{self.backend_url}/api/floats",
                headers=headers,
                timeout=10
            )

            cors_headers = response.headers

            if 'access-control-allow-origin' in cors_headers:
                print("   ✅ CORS Headers Present")
                print(f"   🌐 Allow Origin: {cors_headers.get('access-control-allow-origin')}")
                return True
            else:
                print("   ❌ CORS Headers Missing")
                return False

        except Exception as e:
            print(f"   ❌ CORS Test Error: {e}")
            return False

    def run_full_test_suite(self):
        """Run complete integration test suite"""
        print("🧪 FloatChat Integration Test Suite")
        print("=" * 50)

        tests = [
            ("Backend Health", self.test_backend_health),
            ("API Endpoints", self.test_backend_endpoints),
            ("Chat Functionality", self.test_chat_endpoint),
            ("Frontend Access", self.test_frontend_accessibility),
            ("CORS Configuration", self.test_cors_configuration)
        ]

        passed = 0
        total = len(tests)

        for test_name, test_func in tests:
            if test_func():
                passed += 1

        print("\\n" + "=" * 50)
        print(f"📊 Test Results: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 All tests passed! Integration is working perfectly.")
            print("\\n🚀 Your FloatChat system is ready for use:")
            print("   • Streamlit UI: http://localhost:8502")
            print("   • React UI: http://localhost:5173")
            print("   • Backend API: http://127.0.0.1:8001")
        else:
            print(f"⚠️ {total - passed} tests failed. Please check the issues above.")
            print("\\n🔧 Troubleshooting tips:")
            print("   1. Ensure all services are running")
            print("   2. Check for port conflicts")
            print("   3. Verify network connectivity")

        return passed == total

if __name__ == "__main__":
    tester = IntegrationTester()
    success = tester.run_full_test_suite()
    exit(0 if success else 1)
