import streamlit as st

from components.header import render_header
from components.sidebar import render_sidebar


render_sidebar()

render_header(
    "📄 Documents",
    "Manage uploaded documents.",
)

st.info("Coming soon")
