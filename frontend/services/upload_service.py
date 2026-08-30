from services.api import api


class UploadService:
    """Handle document uploads"""

    def upload(self, filename: str, content: bytes) -> None:
        response = api.upload_document(filename, content)

        response.raise_for_status()


upload_service = UploadService()
