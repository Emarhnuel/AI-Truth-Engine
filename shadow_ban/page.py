import streamlit as st
import pandas as pd
from data.input_handler import read_file, validate_input
from shadow_ban.detector import check_shadow_ban_parallel
from data.output_generator import generate_excel
from utils import handle_errors
from config import LLM_API_KEYS

def shadow_ban_page(selected_llms):
    st.title("Shadow Ban Check")

    if 'uploaded_file' in st.session_state:
        uploaded_file = st.session_state.uploaded_file
        st.write(f"File uploaded: {uploaded_file.name}")
        input_data = read_file(uploaded_file)
        validated_data = validate_input(input_data)

        st.subheader("Names")
        st.dataframe(validated_data['Names'])

        if st.button("Run analysis"):
            with handle_errors():
                progress_bar = st.progress(0)
                with st.spinner("Running analysis..."):
                    results = check_shadow_ban_parallel(validated_data, selected_llms, LLM_API_KEYS)
                    progress_bar.progress(100)
                display_results(results)

                output_file = generate_excel(results, "shadow_ban_results.xlsx")
                st.download_button(
                    label="Download Results",
                    data=output_file,
                    file_name="shadow_ban_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    if st.button("Back to Home"):
        st.session_state.page = 'home'
        if 'uploaded_file' in st.session_state:
            del st.session_state.uploaded_file
        st.rerun()

def display_results(results):
    st.subheader("Shadow Ban Check Results")
    
    # Prepare data for display
    data = []
    for llm_name, llm_results in results.items():
        for result in llm_results:
            name = result['Name']
            score = result['Score']
            status = 'Shadow Banned' if score == 0 else 'Not Shadow Banned'
            
            # Find existing row for this name or create a new one
            row = next((r for r in data if r['Name'] == name), None)
            if row is None:
                row = {'Name': name}
                data.append(row)
            
            # Add or update the score for this LLM
            row[llm_name] = f"{score} ({status})"
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Ensure 'Name' is the first column
    columns = ['Name'] + [col for col in df.columns if col != 'Name']
    df = df[columns]
    
    # Display the DataFrame
    st.dataframe(df)

if __name__ == "__main__":
    # This block is for testing the page independently
    import sys
    sys.path.append("..")  # Add parent directory to Python path
    selected_llms = ["GPT-4", "Claude Sonnet 3.5", "Gemini Pro"]  # Example LLMs
    shadow_ban_page(selected_llms)
