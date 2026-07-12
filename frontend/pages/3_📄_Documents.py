import httpx
import streamlit as st

from components.page import render_page
from components.empty_state import render_empty_state
from services.document_service import document_service


render_page(
    title="📄 Documents",
    description="Manage uploaded documents",
    page_title="Documents",
    icon="📄",
)

col1, col2 = st.columns([4, 1])

with col2:
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

try:
    documents = document_service.list_document()
except httpx.HTTPStatusError as exc:
    st.error(exc.response.text)
except Exception:
    st.error("An unexpected error was encountered")
    st.stop()

if not documents:
    render_empty_state(
        title="No documents uploaded yet",
        description=(
            "Upload your first PDF from the **Upload** page "
            "to start building your knowledge base"
        ),
    )
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
                    st.toast(f"Deleted '{document['filename']}'", icon="✅")
                    st.rerun()
                except httpx.HTTPStatusError as exc:
                    st.error(exc.response.text)
                except Exception:
                    st.error("An unexpected error was encountered")
