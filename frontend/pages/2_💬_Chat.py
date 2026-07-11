import streamlit as st

from components.header import render_header
from components.sidebar import render_sidebar


render_sidebar()

render_header(
    "💬 Chat",
    "Ask questions about your uploaded documents.",
)

st.info("Coming soon")
