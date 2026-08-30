from pathlib import Path
from shutil import copyfileobj
from uuid import uuid4

from fastapi import UploadFile
from loguru import logger

from app.core.config import get_settings
from app.core.exceptions import InvalidDocumentError


class StorageService:
    """Handles document storage on the local filesystem"""

    PDF_SIGNATURE = b"%PDF-"

    def __init__(self) -> None:
        self._settings = get_settings()

    def save_file(self, file: UploadFile) -> tuple[str, Path]:
        """Save an uploaded file and return its generated ID and path"""
        logger.info(f"Saving uploaded file {file.filename}")

        document_id = str(uuid4())
        filename = Path(file.filename or "document.pdf").name
        destination = self._settings.upload_directory / f"{document_id}_{filename}"

        with destination.open("wb") as buffer:
            copyfileobj(file.file, buffer)

        logger.info(f"Stored document '{document_id}' ({destination})")

        return document_id, destination

    def validate_pdf(self, file: UploadFile) -> None:
        """Ensure an upload is labelled as and contains a PDF document."""
        header = file.file.read(len(self.PDF_SIGNATURE))
        file.file.seek(0)

        if file.content_type != "application/pdf" or header != self.PDF_SIGNATURE:
            raise InvalidDocumentError("Only valid PDF files are supported")

    def delete_file(self, path: Path) -> None:
        """Remove an uploaded file if it exists."""
        path.unlink(missing_ok=True)
