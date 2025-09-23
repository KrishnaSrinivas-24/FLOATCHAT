"""
Simple test script to verify the backend components work
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.getcwd())

def test_environment():
    """Test if environment variables are set"""
    print("=== Testing Environment ===")

    db_password = os.getenv("DB_PASSWORD")
    google_api_key = os.getenv("GOOGLE_API_KEY")

    print(f"DB_PASSWORD set: {'Yes' if db_password else 'No'}")
    print(f"GOOGLE_API_KEY set: {'Yes' if google_api_key else 'No'}")

    if not db_password or not google_api_key:
        print("❌ Environment variables not properly set!")
        return False

    print("✅ Environment variables are set")
    return True

def test_dependencies():
    """Test if all required dependencies are available"""
    print("\n=== Testing Dependencies ===")

    try:
        import fastapi
        print("✅ FastAPI available")
    except ImportError:
        print("❌ FastAPI not available")
        return False

    try:
        import uvicorn
        print("✅ Uvicorn available")
    except ImportError:
        print("❌ Uvicorn not available")
        return False

    try:
        import pandas
        print("✅ Pandas available")
    except ImportError:
        print("❌ Pandas not available")
        return False

    try:
        import sqlalchemy
        print("✅ SQLAlchemy available")
    except ImportError:
        print("❌ SQLAlchemy not available")
        return False

    return True

def test_ai_core():
    """Test if AI core components are available"""
    print("\n=== Testing AI Core ===")

    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment loaded")
    except Exception as e:
        print(f"❌ Could not load environment: {e}")
        return False

    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ LangChain Google GenAI available")
    except ImportError as e:
        print(f"❌ LangChain Google GenAI not available: {e}")
        return False

    try:
        from langchain_community.utilities import SQLDatabase
        print("✅ LangChain SQL Database available")
    except ImportError as e:
        print(f"❌ LangChain SQL Database not available: {e}")
        return False

    try:
        from langchain_community.vectorstores import FAISS
        print("✅ LangChain FAISS available")
    except ImportError as e:
        print(f"❌ LangChain FAISS not available: {e}")
        return False

    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        print("✅ HuggingFace Embeddings available")
    except ImportError as e:
        print(f"❌ HuggingFace Embeddings not available: {e}")
        return False

    return True

def test_database_connection():
    """Test database connection"""
    print("\n=== Testing Database Connection ===")

    try:
        from dotenv import load_dotenv
        load_dotenv()

        DB_PASSWORD = os.getenv("DB_PASSWORD")
        if not DB_PASSWORD:
            print("❌ DB_PASSWORD not set")
            return False

        from sqlalchemy import create_engine, text

        db_uri = f"postgresql+psycopg2://postgres:{DB_PASSWORD}@localhost:5432/postgres"
        engine = create_engine(db_uri)

        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")
            return True

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_faiss_index():
    """Test if FAISS index is available"""
    print("\n=== Testing FAISS Index ===")

    import os

    possible_paths = [
        "ai_core/faiss_index",
        "faiss_index",
        os.path.join("ai_core", "faiss_index")
    ]

    for path in possible_paths:
        if os.path.exists(path):
            index_file = os.path.join(path, "index.faiss")
            pkl_file = os.path.join(path, "index.pkl")

            if os.path.exists(index_file) and os.path.exists(pkl_file):
                print(f"✅ FAISS index found at: {path}")
                return True
            else:
                print(f"⚠️  Path exists but missing files: {path}")

    print("❌ FAISS index not found in any expected location")
    return False

if __name__ == "__main__":
    print("🧪 FloatChat Backend Test Suite")
    print("=" * 50)

    tests = [
        test_environment,
        test_dependencies,
        test_ai_core,
        test_database_connection,
        test_faiss_index
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")

    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} passed")

    if passed == total:
        print("🎉 All tests passed! Backend should work correctly.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
