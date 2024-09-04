import streamlit as st
import pandas as pd
from data.input_handler import read_file, validate_input
from shadow_ban.detector import check_shadow_ban
from data.output_generator import generate_excel
from utils import handle_errors

def shadow_ban_page(selected_llms, llm_api_keys):
    st.title("Information Availability Check")

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

                output_file = generate_excel(results, "information_availability_results.xlsx")
                st.download_button(
                    label="Download Results",
                    data=output_file,
                    file_name="information_availability_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    if st.button("Back to Home"):
        st.session_state.page = 'home'
        if 'uploaded_file' in st.session_state:
            del st.session_state.uploaded_file
        st.rerun()

def display_results(results):
    st.subheader("Information Availability Check Results")

    flattened_results = []
    for llm, llm_results in results.items():
        for result in llm_results:
            flattened_results.append(result)

    df = pd.DataFrame(flattened_results)

    columns_order = ['Name', 'LLM', 'Information Availability', 'Bio Word Count', 'Bio Summary']
    df = df[columns_order]

    df['Bio Word Count'] = pd.to_numeric(df['Bio Word Count'], errors='coerce')


    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    styled_df = df.style.highlight_max(subset=numeric_columns, color='lightgreen')
    styled_df = styled_df.highlight_min(subset=numeric_columns, color='lightcoral')

    st.dataframe(styled_df, use_container_width=True)
