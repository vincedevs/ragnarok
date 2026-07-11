from pathlib import Path
from shutil import copyfileobj
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import get_settings


class StorageService:
    """Handles document storage on the local filesystem"""

    def __init__(self) -> None:
        self._settings = get_settings()

    def save_file(self, file: UploadFile) -> tuple[str, Path]:
        """Save an uploaded file and return its generated ID and path"""

        document_id = str(uuid4())
        destination = self._settings.upload_directory / f"{document_id}_{file.filename}"

        with destination.open("wb") as buffer:
            copyfileobj(file.file, buffer)

        return document_id, destination
