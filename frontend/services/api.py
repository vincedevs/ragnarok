from __future__ import annotations

import httpx
from config import API_BASE_URL


class APIClient:
    """HTTP Client for communicating with RAGnarock backend"""

    def __init__(self) -> None:
        self._client = httpx.Client(
            base_url=API_BASE_URL,
            timeout=30.0,
        )

    def health(self) -> bool:
        """Return True if the backend is reachable"""
        try:
            response = self._client.get("/docs")

            return response.status_code == 200
        except httpx.HTTPError:
            return False

    def upload_document(self, filename: str, content: bytes) -> httpx.Response:
        return self._client.post(
            "/upload", files={"file": (filename, content, "application/pdf")}
        )

    def chat(
        self,
        question: str,
        document_ids: list[str] | None = None,
        history: list[dict[str, str]] | None = None,
    ) -> httpx.Response:
        return self._client.post(
            "/chat",
            json={
                "question": question,
                "document_ids": document_ids,
                "history": history or [],
            },
        )

    def list_documents(self) -> httpx.Response:
        return self._client.get("/documents")

    def delete_document(self, document_id: str) -> httpx.Response:
        return self._client.delete(f"/documents/{document_id}")


api = APIClient()
