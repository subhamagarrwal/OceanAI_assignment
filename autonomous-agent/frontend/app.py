import streamlit as st
import sys
import os

# Add the parent directory to sys.path to allow imports from the backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.state import initialize_session_state
from components.sidebar import render_sidebar
from views.ingestion import render_ingestion_view
from views.planning import render_planning_view
from views.coding import render_coding_view

# --- Page Config ---
st.set_page_config(
    page_title="Autonomous QA Agent",
    page_icon="",
    layout="centered"
)

# --- Initialization ---
initialize_session_state()

# --- Sidebar ---
render_sidebar()

# --- Main Content ---
st.title("Autonomous QA Agent-OceanAI assignment")
st.markdown("Build a knowledge base for your content.html and generating Selenium code.")

# --- Views ---
render_ingestion_view()
render_planning_view()
render_coding_view()
