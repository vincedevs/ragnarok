import httpx
import streamlit as st

from components.header import render_header
from components.sidebar import render_sidebar
from services.document_service import document_service

st.set_page_config(page_title="Documents", page_icon="📄")
render_sidebar()
render_header(
    "📄 Documents",
    "Manage uploaded documents.",
)

col1, col2 = st.columns([4, 1])

with col2:
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

try:
    documents = document_service.list_document()
except httpx.HTTPStatusError as exc:
    st.error(exc.response.text)
except Exception as exc:
    st.error(str(exc))
    st.stop()

if not documents:
    st.info("No documents have been uploaded yet")
    st.stop()

for document in documents:
    with st.container(border=True):
        left, right = st.columns([5, 1])

        with left:
            st.subheader(document["filename"])
            st.caption(f"Document ID: `{document['document_id']}`")

        with right:
            if st.button(
                "🗑️ Delete",
                key=document["document_id"],
                type="secondary",
                use_container_width=True,
            ):
                try:
                    document_service.delete_document(document["document_id"])
                    st.success(f"Deleted '{document['filename']}'")
                    st.rerun()
                except httpx.HTTPStatusError as exc:
                    st.error(exc.response.text)
                except Exception as exc:
                    st.error(str(exc))
