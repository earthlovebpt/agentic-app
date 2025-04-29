import streamlit as st
from logger_config import setup_logger
logger = setup_logger()
logger.info("Daisy started.")

st.set_page_config(page_title="Welcome to Daisy", layout="wide")
st.title("👋 Welcome to Daisy")

st.markdown("""
Daisy is your agentic AI business consultant.

**To get started:**
1. Go to **Business and Data Setup** to describe your business and upload your data.
2. Once submitted, you'll be redirected to the **AI Assistant** page where you can ask questions.
""")