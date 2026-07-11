from pathlib import Path

from langchain_core.documents import Document
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

    def build(self, question: str, documents: list[Document]) -> str:
        """Build the prompt"""
        context = "\n\n".join(document.page_content for document in documents)

        return self._prompt.invoke({"context": context, "question": question})
