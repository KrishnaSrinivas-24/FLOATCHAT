# FLOATCHAT

# FloatChat - ARGO Ocean Data Discovery Platform

A comprehensive platform for exploring and analyzing ARGO ocean float data using AI-powered natural language queries and interactive visualizations.

![FloatChat Screenshot](https://via.placeholder.com/800x400/0ea5e9/ffffff?text=FloatChat+Ocean+Data+Platform)

## 🌊 Features

### 🤖 AI-Powered Chat Interface
- Natural language queries about ocean data
- RAG (Retrieval-Augmented Generation) powered responses
- Automatic SQL query generation
- Contextual data analysis and insights

### 📊 Interactive Visualizations
- Real-time ocean float map with trajectory tracking
- Temperature, salinity, and oxygen depth profiles
- Time series analysis and trend visualization
- Data quality assessment tools

### 🛠️ Backend API
- FastAPI-based REST API
- WebSocket support for real-time updates
- Comprehensive data export capabilities
- PostgreSQL database integration

### 🎨 Modern Frontend
- **React Frontend**: Modern TypeScript/React app with shadcn/ui components
- **Streamlit Frontend**: Python-based web interface (currently active)
- Responsive design with interactive maps and charts
- Real-time chat interface with the AI system

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   AI Core       │
│                 │    │                 │    │                 │
│ • React/TS      │◄──►│ • FastAPI       │◄──►│ • LangChain     │
│ • Streamlit     │    │ • WebSocket     │    │ • Google Gemini │
│ • shadcn/ui     │    │ • REST API      │    │ • FAISS Vector  │
│ • Plotly/Maps   │    │ • CORS Support  │    │ • RAG Pipeline  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                ┌─────────────────▼─────────────────┐
                │        Data Layer                 │
                │                                   │
                │ • PostgreSQL Database             │
                │ • ARGO Float NetCDF Files         │
                │ • Curated Knowledge Base          │
                │ • Quality Control Metrics         │
                └───────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL database
- Google Gemini API key
- Node.js 18+ (for React frontend)

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd FLOATCHAT

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the root directory:

```env
# Database Configuration
DB_PASSWORD=your_postgresql_password

# Google AI Configuration
GOOGLE_API_KEY=your_google_gemini_api_key

# Optional: Database URL override
DATABASE_URL=postgresql+psycopg2://postgres:${DB_PASSWORD}@localhost:5432/postgres
```

### 3. Database Setup

```bash
# Ensure PostgreSQL is running
# Create the database and load ARGO data
python data_pipeline/build_database.py

# Create vector embeddings
python ai_core/create_vector_db.py
```

### 4. Start the Backend

Choose one of the following options:

#### Option A: Full Backend (requires database and AI setup)
```bash
python backend_server.py
```

#### Option B: Mock Backend (for testing without full setup)
```bash
python backend_mock.py
```

The backend will be available at:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- WebSocket: ws://localhost:8000/ws

### 5. Start the Frontend

#### Option A: Streamlit Frontend (Currently Active)
```bash
streamlit run streamlit_app.py
```
Access at: http://localhost:8501

#### Option B: React Frontend (requires Node.js)
```bash
cd frontend
npm install
npm run dev
```
Access at: http://localhost:5173

## 💬 Using the Chat Interface

### Example Queries

Try these natural language queries:

```
🌡️ Temperature Analysis:
"Show me temperature profiles near the equator"
"What's the average surface temperature in the Arabian Sea?"
"Compare temperature data between floats 1902672 and 2900464"

🧂 Salinity Studies:
"Find salinity anomalies in the Indian Ocean"
"Show me salinity profiles deeper than 1000m"
"What's the salinity gradient in the upper ocean?"

📍 Location-Based:
"Where are the active floats right now?"
"Show me all floats in the Arabian Sea"
"Which floats are near coordinates 15°N, 68°E?"

📊 Data Quality:
"What's the data quality for float 1902672?"
"Show me floats with recent data"
"Which measurements have the highest quality flags?"
```

### Chat Features

- **Natural Language**: Ask questions in plain English
- **Visual Responses**: Get automatic maps and charts
- **SQL Transparency**: See the generated database queries
- **Confidence Scores**: Understand AI response reliability
- **Interactive Actions**: Click to explore highlighted data

## 🗂️ Project Structure

```
FLOATCHAT/
├── 🎯 Core Application
│   ├── backend_server.py          # Full FastAPI backend
│   ├── backend_mock.py            # Mock backend for testing
│   ├── streamlit_app.py           # Streamlit frontend
│   └── test_backend.py            # Backend testing suite
│
├── 🤖 AI Core
│   ├── ai_core/
│   │   ├── main_agent.py          # RAG pipeline & SQL generation
│   │   ├── curated_knowledge.py   # Knowledge curation
│   │   ├── knowledge_curator.py   # Knowledge base management
│   │   ├── create_vector_db.py    # Vector embeddings creation
│   │   └── faiss_index/           # Vector database
│   │
├── 📊 Data Pipeline
│   ├── data_pipeline/
│   │   ├── build_database.py      # Database construction
│   │   ├── data_quality_checker.py # Quality assessment
│   │   └── attribute_inspector.py # Data exploration
│   │
├── 🎨 React Frontend
│   ├── frontend/
│   │   ├── src/
│   │   │   ├── components/        # React components
│   │   │   ├── services/api.ts    # API integration
│   │   │   └── pages/             # Application pages
│   │   └── package.json           # Dependencies
│   │
├── 🗄️ Data Storage
│   ├── nc files/                  # NetCDF ARGO data
│   └── profiles/                  # Processed profiles
│
└── 📋 Configuration
    ├── requirements.txt           # Python dependencies
    ├── .env                      # Environment variables
    └── README.md                 # This file
```

## 🔧 API Endpoints

### Chat & AI
- `POST /api/chat` - Send natural language queries
- `GET /api/stats` - Database statistics
- `GET /api/quality/{float_id}` - Data quality metrics

### Data Access
- `GET /api/floats` - List all floats with filters
- `GET /api/floats/{float_id}/profile` - Get depth profile
- `GET /api/floats/{float_id}/timeseries` - Time series data
- `GET /api/export` - Export data in various formats

### Real-time
- `WebSocket /ws` - Real-time updates and notifications

## 🎛️ Configuration Options

### Backend Configuration
```python
# backend_server.py
BACKEND_URL = "http://localhost:8000"  # API endpoint
DB_URI = "postgresql+psycopg2://..."   # Database connection
CORS_ORIGINS = ["http://localhost:5173", "http://localhost:8501"]
```

### Frontend Configuration
```typescript
// frontend/src/services/api.ts
baseUrl: 'http://localhost:8000'  # Backend API URL
wsUrl: 'ws://localhost:8000'      # WebSocket URL
```

## 📈 Monitoring & Logs

### Backend Logs
- Server startup and configuration
- API request/response logging
- AI processing steps
- Database query execution
- WebSocket connection status

### Frontend Logs
- API communication status
- Chat interaction history
- Data visualization rendering
- Error handling and recovery

## 🧪 Testing

### Run Backend Tests
```bash
python test_backend.py
```

### Test API Endpoints
```bash
# Test basic connectivity
curl http://localhost:8000/

# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me active floats", "timestamp": "2024-01-01T00:00:00Z"}'

# Test data endpoints
curl http://localhost:8000/api/floats
curl http://localhost:8000/api/stats
```

### Frontend Testing
- Open http://localhost:8501 in your browser
- Try the example queries in the sidebar
- Test map interactions and data visualizations
- Verify chat functionality and responses

## 🚧 Development & Contributing

### Setting Up Development Environment

1. **Database Development**: Use the mock backend for frontend development
2. **AI Development**: Test individual components in `ai_core/`
3. **Frontend Development**: Use either Streamlit or React frontend
4. **API Development**: Use FastAPI's automatic documentation at `/docs`

### Code Style
- **Python**: Follow PEP 8, use type hints
- **TypeScript**: Use strict TypeScript configuration
- **API**: RESTful design with clear error handling
- **Documentation**: Comprehensive docstrings and comments

## 🔮 Future Enhancements

### Planned Features
- [ ] Real-time data streaming from ARGO float networks
- [ ] Advanced machine learning predictions
- [ ] Multi-language support for international users
- [ ] Mobile-responsive progressive web app
- [ ] Integration with additional oceanographic databases
- [ ] Advanced filtering and data mining capabilities
- [ ] Collaborative analysis and sharing features
- [ ] Export to scientific data formats (NetCDF, HDF5)

### Technical Improvements
- [ ] Kubernetes deployment configuration
- [ ] Redis caching for improved performance
- [ ] Advanced error handling and retry logic
- [ ] Comprehensive test suite with CI/CD
- [ ] Database migration system
- [ ] Monitoring and alerting system

## 📞 Support

### Documentation
- API Documentation: http://localhost:8000/docs
- Frontend Documentation: Available in `frontend/README.md`
- Database Schema: See `data_pipeline/` documentation

### Troubleshooting

**Backend Issues:**
- Check environment variables in `.env`
- Verify PostgreSQL connection
- Ensure Google API key is valid
- Check FAISS index exists

**Frontend Issues:**
- Verify backend is running on port 8000
- Check browser console for errors
- Clear Streamlit cache with Ctrl+C, then restart

**Database Issues:**
- Ensure PostgreSQL service is running
- Check database permissions and credentials
- Verify ARGO data files are properly loaded

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🙏 Acknowledgments

- **ARGO Program**: For providing global ocean observations
- **Google Gemini**: AI language model for natural language processing
- **LangChain**: Framework for building AI applications
- **FastAPI**: Modern web framework for building APIs
- **Streamlit**: Framework for creating data applications
- **Plotly**: Interactive visualization library

---

**Built with 🌊 for ocean science and discovery**

The project database is too large to be stored in GitHub. To set up your local database, follow these steps:

1.  **Download the compressed database dump:** [**Click here to download**](https://drive.google.com/file/d/1s2WP4O_WUO_Xrrezdk7VfUJh9SZb0oNi/view?usp=sharing)
2.  **Unzip the file** to get `database_dump.sql`.
3.  **In DBeaver,** open the `.sql` file and run it as a script to create and populate your database.
