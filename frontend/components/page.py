import streamlit as st

from components.header import render_header
from components.sidebar import render_sidebar


def render_page(title: str, description: str, page_title: str, icon: str) -> None:
    st.set_page_config(page_title=page_title, page_icon=icon, layout="wide")
    render_sidebar()
    render_header(title, description)
