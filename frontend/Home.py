import streamlit as st

from components.header import render_header
from components.sidebar import render_sidebar


st.set_page_config(
    page_title="RAGnarok",
    page_icon="⚡",
    layout="wide",
)

render_sidebar()
render_header("⚡ RAGnarok", "Retrieval-Augmented Generation platform")

st.markdown(
    """
    Welcome to **RAGnarok**

    Use the navigation menu on the left to:

    - 📤 Upload PDF documents
    - 💬 Chat with your documents
    - 📄 Manage uploaded documents
    """
)
