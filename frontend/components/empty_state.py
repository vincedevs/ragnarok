import streamlit as st


def render_empty_state(title: str, description: str) -> None:
    st.info(f"### 📂 {title}\n\n{description}", icon="ℹ️")
