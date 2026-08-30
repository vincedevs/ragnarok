from services.api import api


class ChatService:
    """Communicates with the chat endpoint"""

    def ask(self, question: str, document_ids: list[str] | None = None) -> dict:
        response = api.chat(question, document_ids=document_ids)
        response.raise_for_status()

        return response.json()


chat_service = ChatService()
