import streamlit as st
from config import LLM_CONFIGS


def create_sidebar():
    st.sidebar.title("Choose your LLM")
    selected_llms = st.sidebar.multiselect(
        "Select LLMs",
        list(LLM_CONFIGS.keys()),
        default=list(LLM_CONFIGS.keys())[:4]
    )
    return selected_llms

def create_file_uploader(supported_types):
    return st.file_uploader("Choose your options", type=supported_types)

def create_task_selector():
    return st.radio("Choose your task", ["Shadow Ban Check", "Argument Analysis"])

def create_results_display(results):
    st.subheader("Analysis Results")
    st.json(results)
