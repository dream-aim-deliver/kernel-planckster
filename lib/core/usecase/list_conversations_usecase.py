from lib.core.entity.models import Conversation
from lib.core.ports.primary.list_conversations_primary_ports import ListConversationsInputPort
from lib.core.usecase_models.list_conversations_usecase_models import (
    ListConversationsError,
    ListConversationsRequest,
    ListConversationsResponse,
)


class ListConversationsUseCase(ListConversationsInputPort):
    def execute(self, request: ListConversationsRequest) -> ListConversationsResponse | ListConversationsError:
        research_context_id = request.research_context_id
        conversation_1 = Conversation(
            id=1,
            title="Conversation 1",
            created_at="2021-01-01 00:00:00",
            updated_at="2021-01-01 00:00:00",
            deleted=False,
            deleted_at=None,
            conversation_name="Conversation 1",
            research_context_id=request.research_context_id,
        )
        conversation_2 = Conversation(
            id=2,
            title="Conversation 2",
            created_at="2021-01-01 00:00:00",
            updated_at="2021-01-01 00:00:00",
            deleted=False,
            deleted_at=None,
            conversation_name="Conversation 2",
            research_context_id=request.research_context_id,
        )
        return ListConversationsResponse(
            research_context_id=research_context_id, conversations=[conversation_1, conversation_2]
        )
