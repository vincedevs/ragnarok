from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.dependencies import IngestionServiceDep, StorageServiceDep
from app.schemas.upload import UploadResponse

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


@router.post(
    "",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_pdf(
    file: Annotated[UploadFile, File(...)],
    storage_service: StorageServiceDep,
    ingestion_service: IngestionServiceDep,
) -> UploadResponse:
    """Upload a PDF document"""
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported",
        )

    document_id, path = storage_service.save_file(file)

    ingestion_service.ingest(
        document_id=document_id, filename=file.filename, pdf_path=path
    )

    return UploadResponse(
        document_id=document_id,
        filename=file.filename,
        size_bytes=file.size or 0,
        content_type=file.content_type,
    )
