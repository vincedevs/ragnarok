import httpx
import streamlit as st

from components.page import render_page
from components.empty_state import render_empty_state
from services.chat_service import chat_service


render_page(
    title="💬 Chat",
    description="Ask questions about your uploaded documents",
    page_title="Chat",
    icon="💬",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if not st.session_state.messages:
    render_empty_state(
        title="Start a conversation",
        description=("Ask a question about your uploaded documents."),
    )

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
