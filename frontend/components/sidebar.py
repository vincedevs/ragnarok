import streamlit as st

from services.api import api


def render_sidebar() -> None:
    """Render the application sidebar"""
    with st.sidebar:
        st.title("⚡ RAGnarok")
        st.caption("Retrieval-Augmented Generation platform")

        st.divider()

        if api.health():
            st.success("🟢 Backend Connected")
        else:
            st.error("🔴 Backed Offline")
