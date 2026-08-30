from pathlib import Path

from langchain_core.documents import Document
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import ChatPromptTemplate


class PromptService:
    """Builds prompts for question answering"""

    def __init__(self) -> None:
        prompt_dir = Path(__file__).parent.parent / "prompts"
        system_prompt = (prompt_dir / "rag_system.md").read_text(encoding="utf-8")
        user_prompt = (prompt_dir / "rag_user.md").read_text(encoding="utf-8")

        self._prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", user_prompt),
            ]
        )

    def build(self, question: str, documents: list[Document]) -> PromptValue:
        """Build the prompt"""
        context_blocks = []

        for document in documents:
            filename = document.metadata.get("filename", "Unknown document")
            page_number = document.metadata.get("page_number", "Unknown")
            section = document.metadata.get("section_heading")
            source = f"Source: {filename}, page {page_number}"
            if section:
                source += f", section: {section}"
            context_blocks.append(f"[{source}]\n{document.page_content}")

        context = "\n\n".join(context_blocks)

        return self._prompt.invoke({"context": context, "question": question})
