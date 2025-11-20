import streamlit as st
from utils.api_client import APIClient

def initialize_session_state():
    """Initializes the session state variables."""
    if "step" not in st.session_state:
        st.session_state.step = 1
    
    if "test_plan" not in st.session_state:
        st.session_state.test_plan = {}
        
    if "generated_code" not in st.session_state:
        st.session_state.generated_code = {}

def initialize_agent():
    pass # No-op now, backend handles it
