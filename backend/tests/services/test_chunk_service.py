from app.services.chunk_service import ChunkService
from app.services.pdf_service import ExtractedPage


def test_split_text_returns_multiple_chunks() -> None:
    service = ChunkService()

    text = "Hello World! " * 500

    chunks = service.split_text(text)

    assert len(chunks) > 1


def test_split_empty_text_returns_empty_list() -> None:
    service = ChunkService()

    chunks = service.split_text("")

    assert chunks == []


def test_split_pages_creates_section_aware_parent_child_chunks() -> None:
    service = ChunkService()
    pages = [
        ExtractedPage(
            page_number=4,
            text="OVERVIEW\n" + ("Important architecture details. " * 30),
        )
    ]

    chunks = service.split_pages(pages)

    assert len(chunks) > 1
    assert {chunk.page_number for chunk in chunks} == {4}
    assert {chunk.section_heading for chunk in chunks} == {"OVERVIEW"}
    assert {chunk.parent_index for chunk in chunks} == {0}
    assert [chunk.chunk_index for chunk in chunks] == list(range(len(chunks)))
    assert all(chunk.content in chunk.parent_content for chunk in chunks)


def test_split_pages_keeps_numbered_sections_separate() -> None:
    service = ChunkService()
    pages = [
        ExtractedPage(
            page_number=1,
            text="1 Introduction\nIntro text\n2 Architecture\nArchitecture text",
        )
    ]

    chunks = service.split_pages(pages)

    assert [chunk.section_heading for chunk in chunks] == [
        "1 Introduction",
        "2 Architecture",
    ]
    assert [chunk.parent_index for chunk in chunks] == [0, 1]
