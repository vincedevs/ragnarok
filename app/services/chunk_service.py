from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import get_settings

class ChunkService:
    """Splits extracted text into chunks"""
    def __init__(self) -> None:
        settings = get_settings()

        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )

    def split_text(self, text: str) -> list[str]:
        """Splits text into chunks"""
        return self._text_splitter.split_text(text)
