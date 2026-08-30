from typing import Annotated

from fastapi import APIRouter, File, UploadFile, status

from app.core.exceptions import DocumentIngestionError, InvalidDocumentError
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
    storage_service.validate_pdf(file)

    document_id, path = storage_service.save_file(file)

    try:
        ingestion_service.ingest(
            document_id=document_id,
            filename=path.name.removeprefix(f"{document_id}_"),
            pdf_path=path,
        )
    except InvalidDocumentError:
        storage_service.delete_file(path)
        raise
    except Exception as error:
        storage_service.delete_file(path)
        raise DocumentIngestionError(
            "The document could not be indexed. Please try again."
        ) from error

    return UploadResponse(
        document_id=document_id,
        filename=path.name.removeprefix(f"{document_id}_"),
        size_bytes=file.size or 0,
        content_type=file.content_type or "application/pdf",
    )
