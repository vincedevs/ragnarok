from collections.abc import Mapping, Sequence
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
        rewrite_system = (prompt_dir / "rewrite_system.md").read_text(encoding="utf-8")
        rewrite_user = (prompt_dir / "rewrite_user.md").read_text(encoding="utf-8")

        self._prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", user_prompt),
            ]
        )
        self._rewrite_prompt = ChatPromptTemplate.from_messages(
            [("system", rewrite_system), ("human", rewrite_user)]
        )

    def build(self, question: str, documents: list[Document]) -> PromptValue:
        """Build the prompt"""
        context_blocks = []

        for document in documents:
            filename = document.metadata.get("filename", "Unknown document")
            page_number = document.metadata.get("page_number", "Unknown")
            section = document.metadata.get("section_heading")
            source = f"{filename}, p. {page_number}"
            if section:
                source += f", {section}"
            context_blocks.append(f"[{source}]\n{document.page_content}")

        context = "\n\n".join(context_blocks)

        return self._prompt.invoke({"context": context, "question": question})

    def build_rewrite(
        self, question: str, history: Sequence[Mapping[str, str]]
    ) -> PromptValue:
        """Build a prompt that resolves a follow-up into a standalone query."""
        transcript = "\n".join(
            f"{message['role'].title()}: {message['content']}" for message in history
        )
        return self._rewrite_prompt.invoke(
            {"history": transcript, "question": question}
        )
