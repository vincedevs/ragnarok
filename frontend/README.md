# RAGnarok UI

Streamlit frontend for uploading PDFs, chatting with selected documents, inspecting
retrieved sources, and deleting indexed documents.

See the [project README](../README.md) for complete setup instructions. To run only
the frontend:

```bash
uv sync
uv run streamlit run Home.py
```

The backend URL is configured with `FRONTEND_API_URL` in `.env`.
