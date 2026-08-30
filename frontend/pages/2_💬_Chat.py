import httpx
import streamlit as st
from components.empty_state import render_empty_state
from components.page import render_page
from components.sources import render_sources
from services.chat_service import chat_service
from services.document_service import document_service

render_page(
    title="💬 Chat",
    description="Ask questions about your uploaded documents",
    page_title="Chat",
    icon="💬",
)

col1, col2 = st.columns([6, 1])

with col2:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    available_documents = document_service.list_document()
except Exception:
    available_documents = []

document_names = {
    document["document_id"]: document["filename"] for document in available_documents
}
selected_document_ids = st.multiselect(
    "Search specific documents",
    options=list(document_names),
    format_func=lambda document_id: document_names[document_id],
    placeholder="All documents",
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        render_sources(message.get("sources", []))

if not st.session_state.messages:
    render_empty_state(
        title="Start a conversation",
        description="Ask a question about your uploaded documents",
    )

question = st.chat_input("Ask a question...")

if question:
    history = [
        {"role": message["role"], "content": message["content"]}
        for message in st.session_state.messages[-10:]
    ]
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.write(question)

    try:
        with st.spinner("Thinking..."):
            result = chat_service.ask(
                question,
                document_ids=selected_document_ids or None,
                history=history,
            )
    except httpx.HTTPStatusError as exc:
        st.error(exc.response.json()["detail"])
    except Exception:
        st.error("An unexpected error was encountered")
    else:
        sources = result.get("sources", [])
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": result["answer"],
                "sources": sources,
            }
        )

        with st.chat_message("assistant"):
            st.markdown(result["answer"])
            render_sources(sources)
