from services.api import api


class DocumentService:
    """Handle document management"""

    def list_document(self) -> list[dict]:
        response = api.list_documents()
        response.raise_for_status()

        return response.json()

    def delete_document(self, document_id: str) -> None:
        response = api.delete_document(document_id)
        response.raise_for_status()


document_service = DocumentService()
