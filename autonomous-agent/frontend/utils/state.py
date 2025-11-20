import streamlit as st
import sys
import os

# Ensure parent directory is in path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sentence_transformers import SentenceTransformer
from rag.database import vector_store
from rag.retriever import PGVectorRetriever
from rag.engine import RAGQueryEngine
from core.agent import AutonomousQAAgent

def initialize_session_state():
    """Initializes the session state variables."""
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "test_plan" not in st.session_state:
        st.session_state.test_plan = None
    if "generated_code" not in st.session_state:
        st.session_state.generated_code = {}

@st.cache_resource
def initialize_agent():
    """Initializes the RAG components and Agent once."""
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    retriever = PGVectorRetriever(vector_store, embed_model)
    rag_engine = RAGQueryEngine(retriever)
    return AutonomousQAAgent(rag_engine)
