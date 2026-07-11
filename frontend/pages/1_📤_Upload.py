import streamlit as st

from components.header import render_header
from components.sidebar import render_sidebar


render_sidebar()
render_header("📤Upload", "Upload PDF docuiments to build your knowledge base")

st.info("Coming soon!")
