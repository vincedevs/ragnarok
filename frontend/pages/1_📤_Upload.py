import httpx
import streamlit as st

from components.page import render_page
from services.upload_service import upload_service


render_page(
    title="📤 Upload",
    description="Upload PDF docuiments to build your knowledge base",
    page_title="Upload",
    icon="📤",
)

uploaded_file = st.file_uploader("Select a PDF", type=["pdf"])

if uploaded_file is not None:
    st.write(f"**Selected:** {uploaded_file.name}")

    if st.button("Upload", type="primary"):
        with st.spinner("🚀 Uploading document..."):
            try:
                upload_service.upload(
                    filename=uploaded_file.name, content=uploaded_file.getvalue()
                )

                st.toast("Document uploaded successfully!", icon="✅")
            except httpx.HTTPStatusError as exc:
                detail = "❌ Upload failed"

                try:
                    detail = exc.response.json().get("detail", detail)
                except Exception:
                    pass
                st.error(detail)
            except Exception as exc:
                st.error(str(exc))
