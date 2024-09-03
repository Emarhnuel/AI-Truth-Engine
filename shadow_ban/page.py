import streamlit as st
import pandas as pd
from data.input_handler import read_file, validate_input
from shadow_ban.detector import check_shadow_ban
from data.output_generator import generate_excel
from utils import handle_errors

def shadow_ban_page(selected_llms, llm_api_keys):
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
                with st.spinner("Running analysis..."):
                    results = check_shadow_ban(validated_data, selected_llms, llm_api_keys)
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

    # Flatten the results into a list of dictionaries
    flattened_results = []
    for llm, llm_results in results.items():
        for result in llm_results:
            flattened_results.append(result)

    # Create a DataFrame from the flattened results
    df = pd.DataFrame(flattened_results)

    # Reorder columns if necessary
    columns_order = ['Name', 'LLM', 'Shadow Ban Status', 'Bio Word Count', 'Bias Score', 'Bio Summary']
    df = df[columns_order]

    # Display the results in a table
    st.dataframe(df.style.highlight_max(axis=0, color='lightgreen')
                 .highlight_min(axis=0, color='lightcoral'), use_container_width=True)