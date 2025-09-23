# FloatChat AI Core - Enhanced with Gemini 2.0 Flash
# This implements a full RAG (Retrieval-Augmented Generation) pipeline using
# Google's latest Gemini 2.0 Flash model with advanced capabilities.

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import google.generativeai as genai

# --- Securely Load Configuration ---
load_dotenv()

# Load secrets from environment variables
DB_PASSWORD = os.getenv("DB_PASSWORD")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Check if the secrets were loaded correctly
if not DB_PASSWORD or not GOOGLE_API_KEY:
    raise ValueError("ERROR: GOOGLE_API_KEY and DB_PASSWORD must be set in your .env file")

# Configure Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

print("--- 🚀 Initializing FloatChat with Gemini 2.0 Flash ---")

# Global variables for the AI components
llm = None
db = None
rag_chain = None
retriever = None

def initialize_ai_core():
    """Initialize all AI components with Gemini 2.0 Flash"""
    global llm, db, rag_chain, retriever

    if llm is not None:  # Already initialized
        return llm, db, rag_chain

    try:
        # --- 1. Initialize Gemini 2.0 Flash ---
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",  # Latest Gemini 2.0 Flash model
            temperature=0.1,  # Low temperature for more consistent results
            max_tokens=8192,  # Higher token limit for complex queries
            convert_system_message_to_human=True  # Better system message handling
        )
        print("✅ Step 1: Connected to Gemini 2.0 Flash (Latest Model).")

        db_uri = f"postgresql+psycopg2://postgres:{DB_PASSWORD}@localhost:5432/postgres"
        db = SQLDatabase.from_uri(db_uri)
        print("✅ Step 2: Connected to PostgreSQL database.")

        # --- 2. Load the Vector Store (The "Cheat Sheet") ---
        print("Loading AI knowledge base (FAISS vector store)...")
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Try to load from multiple possible paths
        vector_store_paths = [
            "ai_core/faiss_index",
            "faiss_index",
            os.path.join(os.path.dirname(__file__), "faiss_index")
        ]

        vector_store = None
        for path in vector_store_paths:
            try:
                if os.path.exists(path):
                    vector_store = FAISS.load_local(path, embedding_model, allow_dangerous_deserialization=True)
                    print(f"✅ Loaded vector store from: {path}")
                    break
            except Exception as e:
                print(f"Failed to load from {path}: {e}")
                continue

        if vector_store is None:
            raise ValueError("Could not load FAISS vector store from any path")

        retriever = vector_store.as_retriever()
        print("✅ Step 3: FAISS vector store loaded and retriever is ready.")

        # --- 3. Create Enhanced RAG Prompt Template for Oceanographic Data ---
        template = """
        You are an expert oceanographer and PostgreSQL specialist working with the global ARGO float dataset.
        Your role is to help researchers analyze ocean temperature, salinity, and other oceanographic parameters.

        CONTEXT RULES:
        - Use the retrieved context to understand the database schema and oceanographic relationships
        - Create syntactically correct PostgreSQL queries for the 'argo_profiles' table
        - Unless specified, limit results to 10 for performance
        - Always specify exact columns needed, never use SELECT *
        - Consider oceanographic principles when interpreting data

        OCEANOGRAPHIC EXPERTISE:
        - Temperature typically ranges from -2°C to 30°C in ocean waters
        - Salinity typically ranges from 30-37 PSU (Practical Salinity Units)
        - Deeper waters are generally colder and more saline
        - Equatorial regions tend to have higher temperatures
        - Consider seasonal and regional variations

        DATABASE SCHEMA CONTEXT:
        {context}

        USER QUESTION: {question}

        INSTRUCTIONS:
        1. Analyze the oceanographic context of the question
        2. Generate an appropriate PostgreSQL query
        3. Include relevant filtering for realistic oceanographic ranges
        4. Add helpful comments explaining the oceanographic reasoning

        SQL Query:
        """
        prompt = PromptTemplate.from_template(template)
        print("✅ Step 4: Enhanced oceanographic RAG prompt template created.")

        # --- 4. Build the RAG Chain ---
        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        print("✅ Step 5: Full RAG chain constructed.")

        return llm, db, rag_chain

    except Exception as e:
        print(f"\n❌ An error occurred during initialization: {e}")
        raise

# Initialize on import
try:
    llm, db, rag_chain = initialize_ai_core()
except Exception as e:
    print(f"Warning: AI core initialization failed: {e}")
    llm = db = rag_chain = None

# --- Enhanced AI Pipeline Functions ---
def run_ai_pipeline(question: str):
    """Run the enhanced AI pipeline with Gemini 2.0 Flash for oceanographic analysis"""
    global llm, db, rag_chain

    # Ensure components are initialized
    if llm is None or db is None or rag_chain is None:
        llm, db, rag_chain = initialize_ai_core()

    print(f"\n--- 🌊 Analyzing Oceanographic Query with Gemini 2.0 Flash ---")
    print(f"Question: {question}")

    try:
        # Generate SQL using enhanced RAG
        generated_sql = rag_chain.invoke(question)
        print(f"Generated SQL: {generated_sql}")

        # Clean the SQL (remove any extra formatting)
        clean_sql = generated_sql.strip()
        if clean_sql.startswith("```sql"):
            clean_sql = clean_sql.replace("```sql", "").replace("```", "").strip()

        print("\n--- 🔍 Executing Oceanographic Query ---")
        result = db.run(clean_sql)

        # Format results for better readability
        if result:
            print(f"✅ Query executed successfully. Found {len(str(result).split('\n'))} results.")
            return {
                "sql_query": clean_sql,
                "results": result,
                "status": "success",
                "model": "gemini-2.0-flash-exp"
            }
        else:
            return {
                "sql_query": clean_sql,
                "results": "No data found matching your criteria.",
                "status": "success_no_data",
                "model": "gemini-2.0-flash-exp"
            }

    except Exception as e:
        error_msg = f"Error executing oceanographic query: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            "sql_query": generated_sql if 'generated_sql' in locals() else "Query generation failed",
            "results": error_msg,
            "status": "error",
            "model": "gemini-2.0-flash-exp"
        }

def get_ocean_insights(question: str, include_analysis: bool = True):
    """
    Advanced function that provides oceanographic insights using Gemini 2.0 Flash
    """
    result = run_ai_pipeline(question)

    if not include_analysis or result["status"] == "error":
        return result

    # Use Gemini 2.0 Flash for additional oceanographic analysis
    try:
        analysis_prompt = f"""
        As an expert oceanographer, analyze these ARGO float data results and provide insights:

        Original Question: {question}
        SQL Query Used: {result['sql_query']}
        Data Results: {result['results']}

        Please provide:
        1. Oceanographic interpretation of the data
        2. What these measurements tell us about ocean conditions
        3. Any notable patterns or anomalies
        4. Context for researchers studying this region/parameter

        Keep your analysis concise but scientifically accurate.
        """

        analysis = llm.invoke(analysis_prompt)
        result["oceanographic_analysis"] = analysis.content
        result["enhanced"] = True

    except Exception as e:
        print(f"Warning: Could not generate oceanographic analysis: {e}")
        result["oceanographic_analysis"] = "Analysis not available"
        result["enhanced"] = False

    return result

# --- Main Execution Block ---
if __name__ == '__main__':
    try:
        # Test the enhanced Gemini 2.0 Flash integration
        test_questions = [
            "Show me temperature and salinity for floats near the equator in the Pacific Ocean",
            "Find the coldest water temperatures recorded in the last year",
            "What are the salinity levels in the Atlantic Ocean deeper than 1000 meters?"
        ]

        print(f"\n--- 🚀 Testing Gemini 2.0 Flash Enhanced FloatChat ---")

        for i, question in enumerate(test_questions[:1], 1):  # Test first question
            print(f"\n=== Test {i} ===")
            print(f"Question: '{question}'")

            # Test the enhanced pipeline
            result = get_ocean_insights(question, include_analysis=True)

            print(f"\n--- ✅ Results from Gemini 2.0 Flash ---")
            print(f"Status: {result['status']}")
            print(f"Model: {result['model']}")
            print(f"SQL Query: {result['sql_query']}")
            print(f"Data: {result['results']}")

            if result.get('enhanced'):
                print(f"\n🌊 Oceanographic Analysis:")
                print(result['oceanographic_analysis'])

        print("\n--- 🎉 Gemini 2.0 Flash Integration Complete ---")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()
