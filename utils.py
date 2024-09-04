import logging
from contextlib import contextmanager
import streamlit as st

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@contextmanager
def handle_errors():
    try:
        yield
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logging.exception("An error occurred during execution")
