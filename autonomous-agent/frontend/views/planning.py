import streamlit as st
from utils.api_client import APIClient

def render_planning_view():
    """Renders the Phase 2: Test Planning view."""
    if st.session_state.step >= 2:
        st.markdown("---")
        st.subheader("2. Test Case Generation")
        
        user_query = st.text_input(
            "Describe what you want to test", 
            placeholder="e.g., Verify user login functionality with valid and invalid credentials",
            disabled=st.session_state.step > 2
        )
        
        if st.button("Generate Test Plan", type="primary", disabled=st.session_state.step > 2):
            if not user_query:
                st.warning("Please enter a requirement.")
            else:
                with st.spinner("Analyzing Knowledge Base & Generating Scenarios..."):
                    # Call the API
                    result = APIClient.generate_plan(user_query)
                    
                    if "error" in result:
                        st.error(f"Error generating plan: {result['error']}")
                    else:
                        st.session_state.test_plan = result
                        st.session_state.step = 3
                        st.rerun()
