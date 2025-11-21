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
        st.header("Workflow Progress")
        
        phases = [
            (1, "Phase 1: Ingestion"),
            (2, "Phase 2: Planning"),
            (3, "Phase 3: Coding")
        ]
        
        current_step = st.session_state.step
        
        for step_num, label in phases:
            if step_num < current_step:
                # Completed
                st.markdown(
                    f"✅ <span style='color: green; "
                    f"text-decoration: line-through;'>{label}</span>",
                    unsafe_allow_html=True
                )
            elif step_num == current_step:
                # Current
                st.markdown(f"🔵 **{label}**")
            else:
                # Future (Greyed out)
                st.markdown(
                    f"⚪ <span style='color: grey; "
                    f"opacity: 0.5;'>{label}</span>",
                    unsafe_allow_html=True
                )
