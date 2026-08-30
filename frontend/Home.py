import streamlit as st
from components.page import render_page

render_page(
    title="⚡ RAGnarok",
    description="Retrieval-Augmented Generation platform",
    page_title="RAGnarok",
    icon="⚡",
)

st.markdown(
    """
    Welcome to **RAGnarok**

    Use the navigation menu on the left to:

    - 📤 Upload PDF documents
    - 💬 Chat with your documents
    - 📄 Manage uploaded documents
    """
)
