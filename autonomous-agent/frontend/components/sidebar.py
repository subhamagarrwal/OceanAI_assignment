import streamlit as st

def render_sidebar():
    """Renders the sidebar controls and status."""
    with st.sidebar:
        st.header("⚙️ Controls")
        if st.button("Reset Application", type="primary"):
            st.session_state.step = 1
            st.session_state.test_plan = None
            st.session_state.generated_code = {}
            st.rerun()
        
        st.markdown("---")
        st.markdown("**Status:**")
        if st.session_state.step == 1:
            st.info("Phase 1: Ingestion")
        elif st.session_state.step == 2:
            st.info("Phase 2: Planning")
        elif st.session_state.step >= 3:
            st.success("Phase 3: Coding")
