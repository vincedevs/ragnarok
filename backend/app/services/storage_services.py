from pathlib import Path
from shutil import copyfileobj
from uuid import uuid4

from backend.app.core.config import get_settings
from fastapi import UploadFile
from loguru import logger


class StorageService:
    """Handles document storage on the local filesystem"""

    def __init__(self) -> None:
        self._settings = get_settings()

    def save_file(self, file: UploadFile) -> tuple[str, Path]:
        """Save an uploaded file and return its generated ID and path"""
        logger.info(f"Saving uploaded file {file.filename}")

        document_id = str(uuid4())
        destination = self._settings.upload_directory / f"{document_id}_{file.filename}"

        with destination.open("wb") as buffer:
            copyfileobj(file.file, buffer)

        logger.info(f"Stored document '{document_id}' ({destination})")

        return document_id, destination
