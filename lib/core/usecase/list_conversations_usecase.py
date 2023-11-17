from lib.core.ports.primary.list_conversations_primary_ports import ListConversationsInputPort
from lib.core.usecase_models.list_conversations_usecase_models import (
    ListConversationsError,
    ListConversationsRequest,
    ListConversationsResponse,
)


class ListConversationsUseCase(ListConversationsInputPort):
    def execute(self, request: ListConversationsRequest) -> ListConversationsResponse | ListConversationsError:
        return ListConversationsResponse(
            research_context_id=request.research_context_id,
            conversations=[
                {
                    "conversation_id": 1,
                    "conversation_name": "Conversation 1",
                    "research_context_id": request.research_context_id,
                },
                {
                    "conversation_id": 2,
                    "conversation_name": "Conversation 2",
                    "research_context_id": request.research_context_id,
                },
            ],
        )
