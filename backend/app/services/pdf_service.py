from pathlib import Path

from backend.app.core.exceptions import InvalidDocumentError
from langchain_community.document_loaders import PyPDFLoader


class PDFService:
    """Extract text from PDF documents"""

    def extract_text(self, pdf_path: Path) -> str:
        """Extract and concatenate text from all pages of a PDF file"""
        try:
            loader = PyPDFLoader(str(pdf_path))
            documents = loader.load()
        except Exception as error:
            raise InvalidDocumentError(str(error)) from error

        return "\n\n".join(
            document.page_content
            for document in documents
            if document.page_content.strip()
        )
