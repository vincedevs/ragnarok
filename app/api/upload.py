from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.schemas.upload import UploadResponse
from app.services.storage_services import StorageService

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

storage_service = StorageService()


@router.post(
    "",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_pdf(file: Annotated[UploadFile, File(...)]) -> UploadResponse:
    """Upload a PDF document"""
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported",
        )

    document_id, _ = storage_service.save_file(file)

    return UploadResponse(
        document_id=document_id,
        filename=file.filename,
        size_bytes=file.size or 0,
        content_type=file.content_type,
    )
