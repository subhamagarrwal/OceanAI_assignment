import streamlit as st
from utils.api_client import APIClient
import io

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
                    st.write("Uploading and processing documents...")
                    
                    files_to_upload = []
                    
                    # Prepare uploaded files
                    if uploaded_files:
                        for f in uploaded_files:
                            files_to_upload.append(('files', (f.name, f.getvalue(), f.type)))
                    
                    # Prepare HTML content as a file
                    if html_content:
                        html_file = io.BytesIO(html_content.encode('utf-8'))
                        files_to_upload.append(('files', ('checkout.html', html_file, 'text/html')))
                    
                    # Call API
                    success = APIClient.upload_files(files_to_upload)
                    
                    if success:
                        status.update(label="Knowledge Base Built Successfully!", state="complete", expanded=False)
                        st.success("Knowledge Base Ready!")
                        st.session_state.step = 2
                        st.rerun()
                    else:
                        status.update(label="Failed to build Knowledge Base", state="error")
                        st.error("Backend API connection failed. Make sure the backend is running.")
