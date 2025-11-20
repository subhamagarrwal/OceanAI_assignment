import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Models
MODEL_TC = "llama-3.3-70b-versatile"
MODEL_CODE = "qwen/qwen3-32b"

# Database
DB_USER = os.getenv("PG_USER", "myuser")
DB_PASS = os.getenv("PG_PASS", "password")
DB_NAME = os.getenv("PG_DB", "rag_db")
DB_HOST = os.getenv("PG_HOST", "localhost")
DB_PORT = os.getenv("PG_PORT", "5432")
VECTOR_TABLE = os.getenv("VECTOR_TABLE", "rag_nodes")

# Embeddings
EMBED_DIM = 384
