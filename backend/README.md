# RAGnarok API

FastAPI backend for PDF ingestion, page-aware parent-child chunking, hybrid
retrieval, and grounded OpenAI answers.

See the [project README](../README.md) for setup, configuration, architecture, and
development commands.

Run the backend by itself from this directory:

```bash
uv sync --dev
uv run uvicorn app.main:app --reload
```
