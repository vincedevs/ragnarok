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


api = APIClient()
