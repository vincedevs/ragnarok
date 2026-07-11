import streamlit as st


def render_header(title: str, description: str) -> None:
    st.title(title)
    st.caption(description)
    st.divider()
