from app.services.chunk_service import ChunkService


def test_split_text_returns_multiple_chunks() -> None:
    service = ChunkService()

    text = "Hello World! " * 500

    chunks = service.split_text(text)

    assert len(chunks) > 1


def test_split_empty_text_returns_empty_list() -> None:
    service = ChunkService()

    chunks = service.split_text("")

    assert chunks == []
