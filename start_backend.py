#!/usr/bin/env python3
"""
Simple backend starter for FloatChat
"""
import uvicorn
from backend_mock import app

if __name__ == "__main__":
    print("Starting FloatChat Backend on http://127.0.0.1:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=False)
