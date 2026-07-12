import httpx
import streamlit as st

from components.header import render_header
from components.sidebar import render_sidebar
from services.chat_service import chat_service

st.set_page_config(page_title="Chat", page_icon="💬")
render_sidebar()
render_header(
    "💬 Chat",
    "Ask questions about your uploaded documents.",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.write(question)

    try:
        with st.spinner("Thinking..."):
            result = chat_service.ask(question)
    except httpx.HTTPStatusError as exc:
        st.error(exc.response.json()["detail"])
    except Exception as exc:
        st.error(str(exc))
    else:
        st.session_state.messages.append(
            {"role": "assistant", "content": result["answer"]}
        )

        with st.chat_message("assistant"):
            st.markdown(result["answer"])

            sources = result.get("sources", [])

            if sources:
                with st.expander("Retrieved Sources", expanded=False):
                    for source in sources:
                        st.write(
                            f"📄 {source['filename']} (chunk {source['chunk_index']})"
                        )
