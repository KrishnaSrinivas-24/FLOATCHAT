"""
FloatChat Backend API Server - Mock Mode
========================================
This version runs without requiring the database or AI core to be set up.
Perfect for testing frontend integration.
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import pandas as pd

# === Pydantic Models ===

class ChatRequest(BaseModel):
    message: str
    filters: Optional[Dict[str, Any]] = None
    timestamp: str

class ChatResponse(BaseModel):
    reply: str
    actions: List[Dict[str, Any]] = []
    sql_query: Optional[str] = None
    confidence: float

class ArgoFloat(BaseModel):
    id: str
    lat: float
    lon: float
    last_contact: str
    temperature: Optional[float] = None
    salinity: Optional[float] = None
    trajectory: List[List[float]] = []
    status: str

class ArgoProfile(BaseModel):
    float_id: str
    variable: str
    depth: List[float]
    values: List[float]
    timestamps: List[str]
    quality_flags: List[int]

# === Global Variables ===
connected_websockets: List[WebSocket] = []

# === FastAPI App ===
app = FastAPI(
    title="FloatChat API - Mock Mode",
    description="Backend API for ARGO Ocean Data Discovery Platform (Mock Mode)",
    version="1.0.0-mock"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Mock Data ===

def get_mock_floats():
    """Generate mock ARGO float data"""
    return [
        {
            "id": "1902672",
            "lat": 15.5,
            "lon": 68.2,
            "last_contact": "2024-01-15T10:30:00Z",
            "temperature": 28.5,
            "salinity": 35.4,
            "trajectory": [[15.1, 67.9], [15.3, 68.0], [15.5, 68.2]],
            "status": "active"
        },
        {
            "id": "1902677",
            "lat": 8.1,
            "lon": 72.3,
            "last_contact": "2024-01-14T15:45:00Z",
            "temperature": 29.2,
            "salinity": 35.1,
            "trajectory": [[7.8, 72.0], [7.9, 72.1], [8.1, 72.3]],
            "status": "active"
        },
        {
            "id": "2900464",
            "lat": -2.1,
            "lon": 85.6,
            "last_contact": "2024-01-13T08:20:00Z",
            "temperature": 27.8,
            "salinity": 35.7,
            "trajectory": [[-2.4, 85.3], [-2.2, 85.4], [-2.1, 85.6]],
            "status": "active"
        },
        {
            "id": "2900533",
            "lat": 22.4,
            "lon": 59.8,
            "last_contact": "2024-01-12T12:15:00Z",
            "temperature": 26.8,
            "salinity": 36.1,
            "trajectory": [[22.1, 59.5], [22.2, 59.6], [22.4, 59.8]],
            "status": "active"
        },
        {
            "id": "2902201",
            "lat": 5.2,
            "lon": 95.4,
            "last_contact": "2024-01-11T09:30:00Z",
            "temperature": 28.9,
            "salinity": 34.8,
            "trajectory": [[5.0, 95.2], [5.1, 95.3], [5.2, 95.4]],
            "status": "delayed"
        }
    ]

def generate_mock_chat_response(message: str) -> ChatResponse:
    """Generate mock chat responses based on message content"""
    message_lower = message.lower()

    if "temperature" in message_lower or "warm" in message_lower:
        return ChatResponse(
            reply="Based on recent ARGO float data, I found interesting temperature patterns in the Arabian Sea. The surface temperatures have been averaging 28.5°C, which is slightly above the seasonal average. Float 1902672 shows a warming trend over the past week.",
            actions=[
                {"type": "highlight", "data": {"float_ids": ["1902672", "1902677"]}},
                {"type": "visualize", "data": {"type": "temperature_map"}}
            ],
            sql_query="SELECT wmo, temperature, lat, lon FROM argo_profiles WHERE variable = 'TEMP' AND lat BETWEEN 10 AND 25",
            confidence=0.89
        )

    elif "salinity" in message_lower or "salt" in message_lower:
        return ChatResponse(
            reply="Salinity measurements from the active floats show normal variations. Current surface salinity ranges from 34.8 to 36.1 PSU in the monitored regions. Float 2900533 in the Arabian Sea shows the highest salinity at 36.1 PSU.",
            actions=[
                {"type": "compare", "data": {"float_ids": ["2900533", "2902201"]}},
                {"type": "visualize", "data": {"type": "salinity_profile"}}
            ],
            sql_query="SELECT wmo, salinity, lat, lon FROM argo_profiles WHERE variable = 'PSAL'",
            confidence=0.92
        )

    elif "location" in message_lower or "map" in message_lower or "where" in message_lower:
        return ChatResponse(
            reply="I'm showing you the locations of our active ARGO floats. We currently have 5 active floats monitoring the Indian Ocean and Arabian Sea. You can see their positions and recent trajectories on the map.",
            actions=[
                {"type": "highlight", "data": {"float_ids": ["1902672", "1902677", "2900464", "2900533", "2902201"]}},
            ],
            confidence=0.95
        )

    elif "profile" in message_lower or "depth" in message_lower:
        return ChatResponse(
            reply="Here are the vertical profiles from our most active floats. The data shows typical ocean stratification with warmer temperatures at the surface decreasing with depth. The thermocline is clearly visible around 100-200m depth.",
            actions=[
                {"type": "visualize", "data": {"type": "depth_profile"}},
                {"type": "compare", "data": {"float_ids": ["1902672", "2900464"]}}
            ],
            confidence=0.88
        )

    elif "equator" in message_lower:
        return ChatResponse(
            reply="Near the equator, Float 2900464 is providing excellent data. The equatorial region shows minimal temperature variation at the surface (around 27.8°C) but interesting subsurface dynamics. The salinity is relatively stable at 35.7 PSU.",
            actions=[
                {"type": "highlight", "data": {"float_ids": ["2900464"]}},
                {"type": "visualize", "data": {"type": "equatorial_analysis"}}
            ],
            sql_query="SELECT * FROM argo_profiles WHERE lat BETWEEN -5 AND 5",
            confidence=0.91
        )

    else:
        return ChatResponse(
            reply="I can help you analyze ARGO float data! Try asking about:\n• Temperature profiles and trends\n• Salinity measurements\n• Float locations and trajectories\n• Depth profiles\n• Specific regions like 'near the equator'\n\nWhat would you like to explore?",
            actions=[],
            confidence=0.75
        )

def generate_mock_profile(float_id: str, variable: str) -> ArgoProfile:
    """Generate mock profile data"""
    depths = [0, 10, 20, 50, 100, 200, 500, 1000, 1500, 2000]

    if variable == "temperature":
        # Realistic temperature profile
        values = [28.5, 28.2, 27.8, 26.5, 24.2, 18.5, 8.2, 4.1, 2.8, 2.1]
    elif variable == "salinity":
        # Realistic salinity profile
        values = [35.1, 35.2, 35.3, 35.4, 35.5, 35.3, 34.8, 34.6, 34.7, 34.8]
    elif variable == "oxygen":
        # Realistic oxygen profile
        values = [245, 240, 235, 210, 180, 150, 120, 100, 90, 85]
    else:
        values = [28.0 + i * -0.5 for i in range(len(depths))]

    timestamps = [datetime.now().isoformat() for _ in depths]

    return ArgoProfile(
        float_id=float_id,
        variable=variable,
        depth=depths,
        values=values,
        timestamps=timestamps,
        quality_flags=[1] * len(depths)
    )

# === API Endpoints ===

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "FloatChat Backend API - Mock Mode",
        "status": "active",
        "mode": "mock",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint with mock RAG integration"""
    try:
        print(f"📩 Received chat request: {request.message}")

        # Generate mock response
        response = generate_mock_chat_response(request.message)

        # Broadcast to WebSocket clients
        if connected_websockets:
            await broadcast_to_websockets({
                "type": "chat_response",
                "data": response.dict()
            })

        return response

    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")
        return ChatResponse(
            reply=f"I encountered an error processing your request: {str(e)}",
            actions=[],
            confidence=0.5
        )

@app.get("/api/floats")
async def get_floats(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    lat_min: Optional[float] = None,
    lat_max: Optional[float] = None,
    lon_min: Optional[float] = None,
    lon_max: Optional[float] = None,
    variable: Optional[str] = None,
    float_id: Optional[str] = None
):
    """Get ARGO float data with optional filters"""
    try:
        floats = get_mock_floats()

        # Apply filters if provided
        if lat_min is not None:
            floats = [f for f in floats if f['lat'] >= lat_min]
        if lat_max is not None:
            floats = [f for f in floats if f['lat'] <= lat_max]
        if lon_min is not None:
            floats = [f for f in floats if f['lon'] >= lon_min]
        if lon_max is not None:
            floats = [f for f in floats if f['lon'] <= lon_max]
        if float_id:
            floats = [f for f in floats if f['id'] == float_id]

        return floats

    except Exception as e:
        print(f"❌ Floats endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/floats/{float_id}/profile")
async def get_float_profile(float_id: str, variable: str = "temperature"):
    """Get profile data for a specific float"""
    try:
        profile = generate_mock_profile(float_id, variable)
        return profile
    except Exception as e:
        print(f"❌ Profile endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/floats/{float_id}/timeseries")
async def get_timeseries(float_id: str, variable: str = "temperature", days: int = 30):
    """Get time series data for a specific float"""
    try:
        # Generate mock time series data
        now = datetime.now()
        data = []

        for i in range(days):
            date = now - timedelta(days=i)
            data.append({
                "timestamp": date.isoformat(),
                variable: 28.0 + (i * 0.1) + (i % 3) * 0.5,  # Simulate variation
                "depth": 10.0 + (i % 5) * 5.0
            })

        return {"float_id": float_id, "data": data}

    except Exception as e:
        print(f"❌ Timeseries endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_database_stats():
    """Get database statistics"""
    return {
        "total_floats": 5,
        "active_floats": 4,
        "total_profiles": 12847,
        "last_update": datetime.now().isoformat()
    }

@app.get("/api/quality/{float_id}")
async def get_data_quality(float_id: str = None):
    """Get data quality metrics"""
    return {
        "overall_quality": 0.94,
        "temperature_quality": 0.96,
        "salinity_quality": 0.92,
        "missing_data_percentage": 0.08,
        "details": f"Quality assessment for float {float_id if float_id else 'all floats'} completed"
    }

@app.get("/api/export")
async def export_data(
    format: str = "csv",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    lat_min: Optional[float] = None,
    lat_max: Optional[float] = None,
    lon_min: Optional[float] = None,
    lon_max: Optional[float] = None
):
    """Export filtered data"""
    try:
        # Generate mock export data
        floats = get_mock_floats()
        df = pd.DataFrame(floats)

        if format == "csv":
            csv_data = df.to_csv(index=False)
            return StreamingResponse(
                iter([csv_data]),
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=argo_data.csv"}
            )
        elif format == "json":
            return JSONResponse(content=floats)
        else:
            raise HTTPException(status_code=400, detail="Unsupported format")

    except Exception as e:
        print(f"❌ Export endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# === WebSocket Support ===

async def broadcast_to_websockets(message: dict):
    """Broadcast message to all connected WebSocket clients"""
    if not connected_websockets:
        return

    disconnected = []
    for ws in connected_websockets:
        try:
            await ws.send_json(message)
        except WebSocketDisconnect:
            disconnected.append(ws)
        except Exception as e:
            print(f"WebSocket send error: {e}")
            disconnected.append(ws)

    # Remove disconnected clients
    for ws in disconnected:
        if ws in connected_websockets:
            connected_websockets.remove(ws)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    connected_websockets.append(websocket)

    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connection",
            "message": "Connected to FloatChat backend (Mock Mode)",
            "timestamp": datetime.now().isoformat()
        })

        # Keep connection alive
        while True:
            try:
                data = await websocket.receive_json()

                # Echo back for now
                await websocket.send_json({
                    "type": "echo",
                    "data": data,
                    "timestamp": datetime.now().isoformat()
                })

            except WebSocketDisconnect:
                break
            except Exception as e:
                print(f"WebSocket error: {e}")
                break

    finally:
        if websocket in connected_websockets:
            connected_websockets.remove(websocket)

# === Development Server ===
if __name__ == "__main__":
    print("🌊 Starting FloatChat Backend Server (Mock Mode)...")
    print("📡 API Documentation: http://localhost:8000/docs")
    print("🔌 WebSocket: ws://localhost:8000/ws")
    print("🧪 Running in mock mode - no database or AI required!")

    uvicorn.run(
        "backend_mock:app",
        host="127.0.0.1",
        port=8001,
        reload=False,  # Disable reload to prevent multiprocessing issues
        log_level="info"
    )
