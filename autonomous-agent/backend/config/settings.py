import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Models
MODEL_TC = "llama-3.3-70b-versatile"
MODEL_CODE = "llama-3.3-70b-versatile"

# Database 
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
if CONNECTION_STRING:
    CONNECTION_STRING = CONNECTION_STRING.strip().strip('"').strip("'")
    parsed = urlparse(CONNECTION_STRING)
    DB_USER = parsed.username
    DB_PASS = parsed.password
    DB_HOST = parsed.hostname
    DB_PORT = str(parsed.port) if parsed.port else "5432"
    DB_NAME = parsed.path[1:] if parsed.path else "postgres"
    
    # Debug: Verify parsed values
    print(f"[DEBUG] Parsed DB config:")
    print(f"  Host: {DB_HOST}")
    print(f"  Port: {DB_PORT}")
    print(f"  Database: {DB_NAME}")
    print(f"  User: {DB_USER}")
    print(f"  Password: {'*' * len(DB_PASS) if DB_PASS else 'None'}")
else:
    # Fallback to individual env vars
    DB_USER = os.getenv("PG_USER", "myuser")
    DB_PASS = os.getenv("PG_PASS", "password")
    DB_NAME = os.getenv("PG_DB", "rag_db")
    DB_HOST = os.getenv("PG_HOST", "localhost")
    DB_PORT = os.getenv("PG_PORT", "5432")

VECTOR_TABLE = os.getenv("VECTOR_TABLE", "rag_nodes")

# Embeddings dimension
EMBED_DIM = 384
