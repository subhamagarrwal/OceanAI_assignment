import streamlit as st
from utils.api_client import APIClient

def render_coding_view():
    """Renders the Phase 3: Selenium Script Generation view."""
    if st.session_state.step >= 3:
        st.markdown("---")
        st.subheader("3. Selenium Script Generator")
        
        test_plan = st.session_state.test_plan
        test_cases = test_plan.get("test_cases", [])
        
        if not test_cases:
            st.error("No test cases found in the plan.")
        else:
            # Display Test Plan Summary
            with st.expander("📄 View Generated Test Plan", expanded=False):
                st.json(test_plan)
                
            # Selection
            tc_options = {f"{tc.get('id')} - {tc.get('title')}": tc for tc in test_cases}
            selected_option = st.selectbox("Select a Test Case to Automate", list(tc_options.keys()))
            
            selected_tc = tc_options[selected_option]
            tc_id = selected_tc.get('id')
            
            if st.button("Generate Selenium Script", type="primary"):
                with st.spinner(f"Writing Python code for {tc_id}..."):
                    
                    # Check if we already generated it
                    if tc_id in st.session_state.generated_code:
                        code = st.session_state.generated_code[tc_id]
                    else:
                        # Call API
                        code = APIClient.generate_code(selected_tc)
                        st.session_state.generated_code[tc_id] = code
                    
                    st.success(f"Script generated for {tc_id}!")
            
            # Display Code if available
            if tc_id in st.session_state.generated_code:
                st.markdown(f"### 🐍 Generated Code: {tc_id}")
                st.code(st.session_state.generated_code[tc_id], language="python")
