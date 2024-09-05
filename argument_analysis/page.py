import streamlit as st
from argument_analysis.analyzer import analyze_argument
from utils import handle_errors
from config import ANALYSIS_TYPES, LLM_CONFIGS, LLM_API_KEYS
import json
import base64

def argument_analysis_page(selected_llms):
    st.title("ARGUMENT ANALYSIS")

    analysis_types = st.multiselect(
        "Select the Types of Analysis",
        ANALYSIS_TYPES,
        default=["Argument Parser", "Logical Analysis Engine"]
    )

    user_argument = st.text_area("Input Your Argument")

    if st.button("Analyze", key="analyze_button"):
        if not analysis_types:
            st.error("Please select at least one type of analysis.")
        elif not user_argument:
            st.error("Please input an argument to analyze.")
        else:
            with handle_errors():
                with st.spinner("Analyzing..."):
                    results = analyze_argument(user_argument, analysis_types, selected_llms, LLM_API_KEYS)
                display_results(results)
                download_results(results)

    if st.button("Back to Home", key="back_to_home_button"):
        st.session_state.page = 'home'
        st.rerun()

def display_results(results):
    st.subheader("Analysis Results")
    for llm, analyses in results.items():
        with st.expander(f"{llm} Analysis"):
            for analysis_type, analysis in analyses.items():
                st.markdown(f"**{analysis_type}:**")
                st.write(analysis)
                st.markdown("---")

def download_results(results):
    # Convert results to JSON
    json_results = json.dumps(results, indent=2)
    
    # Encode to base64
    b64 = base64.b64encode(json_results.encode()).decode()
    
    # Create download link
    href = f'<a href="data:application/json;base64,{b64}" download="analysis_results.json">Download Results (JSON)</a>'
    st.markdown(href, unsafe_allow_html=True)
