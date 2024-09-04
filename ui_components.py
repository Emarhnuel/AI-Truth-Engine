import streamlit as st
from config import LLM_CONFIGS


def create_sidebar():
    st.sidebar.title("Choose your LLM")
    selected_llms = st.sidebar.multiselect(
        "Select LLMs",
        list(LLM_CONFIGS.keys()),
        default=list(LLM_CONFIGS.keys())[:4]
    )

    llm_api_keys = {}
    groq_api_key = st.sidebar.text_input("Groq API Key", type="password")

    for llm in selected_llms:
        if LLM_CONFIGS[llm]["class"] == "Groq":
            llm_api_keys[llm] = groq_api_key
        elif LLM_CONFIGS[llm]["class"] == "Gemini":
            llm_api_keys[llm] = st.sidebar.text_input("Gemini API Key", type="password")
        elif LLM_CONFIGS[llm]["class"] not in ["Groq", "Gemini"]:
            llm_api_keys[llm] = st.sidebar.text_input(f"{llm} API Key", type="password")

    return selected_llms, llm_api_keys

def create_file_uploader(supported_types):
    return st.file_uploader("Choose your options", type=supported_types)

def create_task_selector():
    return st.radio("Choose your task", ["Shadow Ban Check", "Argument Analysis"])

def create_results_display(results):
    st.subheader("Analysis Results")
    st.json(results)
