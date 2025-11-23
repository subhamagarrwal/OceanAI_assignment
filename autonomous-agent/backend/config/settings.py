import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Models
MODEL_TC = "llama-3.3-70b-versatile"
MODEL_CODE = "llama-3.3-70b-versatile"
