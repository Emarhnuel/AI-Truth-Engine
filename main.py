import streamlit as st
from config import APP_TITLE, LLM_API_KEYS
from ui_components import create_sidebar, create_task_selector
from shadow_ban.page import shadow_ban_page
from argument_analysis.page import argument_analysis_page

# Define the favicon
favicon = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
    <rect width="100" height="100" rx="20" fill="#f0f0f0"/>
    <path d="M50 10 C25 10 10 30 10 50 C10 75 30 90 50 90 C70 90 90 75 90 50 C90 30 75 10 50 10 Z" fill="#4a4a4a"/>
    <path d="M40 50 L50 60 L70 40" stroke="white" stroke-width="8" fill="none"/>
    <circle cx="30" cy="40" r="5" fill="white"/>
    <circle cx="70" cy="40" r="5" fill="white"/>
</svg>
"""

def main():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=favicon,
        layout="wide"
    )

    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    selected_llms = create_sidebar()

    if st.session_state.page == 'home':
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("<h1 style='color: #FF0000;'>AI Truth Engine</h1>", unsafe_allow_html=True)

            if st.button("Shadow Ban Check"):
                if 'uploaded_file' in st.session_state and st.session_state.uploaded_file:
                    st.session_state.page = 'shadow_ban'
                    st.rerun()
                else:
                    st.error("Please upload a file before proceeding.")

            if st.button("Argument Analysis"):
                st.session_state.page = 'argument_analysis'
                st.rerun()

        with col2:
            st.header("Choose your options")
            uploaded_file = st.file_uploader("Drag and Drop file here", type=["csv", "xlsx", "xls"])
            if uploaded_file:
                st.session_state.uploaded_file = uploaded_file

    elif st.session_state.page == 'shadow_ban':
        shadow_ban_page(selected_llms)
    elif st.session_state.page == 'argument_analysis':
        argument_analysis_page(selected_llms)

if __name__ == "__main__":
    main()
