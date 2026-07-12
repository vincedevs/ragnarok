from services.api import api


class ChatService:
    """Communicates with the chat endpoint"""

    def ask(self, question: str) -> dict:
        response = api.chat(question)
        response.raise_for_status()

        return response.json()


chat_service = ChatService()
