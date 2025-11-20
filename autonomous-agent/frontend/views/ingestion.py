import streamlit as st
from pathlib import Path
from utils.state import initialize_agent
from rag.ingestion import ingest_documents

def render_ingestion_view():
    """Renders the Phase 1: Knowledge Base Ingestion view."""
    if st.session_state.step >= 1:
        st.subheader("1. Knowledge Base Setup")
        
        col1, col2 = st.columns(2)
        
        with col1:
            uploaded_files = st.file_uploader(
                "Upload Support Documents", 
                type=['txt', 'md', 'json', 'pdf'], 
                accept_multiple_files=True
            )
        
        with col2:
            html_content = st.text_area(
                "Paste checkout.html Content", 
                height=150,
                placeholder="<html>...</html>"
            )

        if st.button("Build Knowledge Base", type="primary", disabled=st.session_state.step > 1):
            if not uploaded_files and not html_content:
                st.error("Please upload documents or paste HTML content.")
            else:
                with st.status("Building Knowledge Base...", expanded=True) as status:
                    # 1. Initialize Agent
                    st.write("Initializing Agent components...")
                    if st.session_state.agent is None:
                        st.session_state.agent = initialize_agent()
                    
                    agent = st.session_state.agent
                    # Access embed_model from the initialized agent
                    embed_model = agent.rag_engine.retriever.embed_model
                    
                    # 2. Process Files
                    temp_dir = Path("temp_uploads")
                    temp_dir.mkdir(exist_ok=True)
                    
                    # Save uploaded files temporarily
                    if uploaded_files:
                        st.write(f"Processing {len(uploaded_files)} documents...")
                        for uploaded_file in uploaded_files:
                            file_path = temp_dir / uploaded_file.name
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            
                            # Ingest
                            ingest_documents(str(file_path), embed_model)
                            st.write(f"Ingested: {uploaded_file.name}")

                    # Save HTML
                    if html_content:
                        st.write("Processing HTML content...")
                        html_path = temp_dir / "checkout.html"
                        with open(html_path, "w", encoding="utf-8") as f:
                            f.write(html_content)
                        
                        ingest_documents(str(html_path), embed_model)
                        st.write("Ingested: checkout.html")
                    
                    status.update(label="Knowledge Base Built Successfully!", state="complete", expanded=False)
                
                st.success("Knowledge Base Ready!")
                st.session_state.step = 2
                st.rerun()
