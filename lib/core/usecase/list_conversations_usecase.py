from lib.core.dto.research_context_repository_dto import ListResearchContextConversationsDTO
from lib.core.ports.primary.list_conversations_primary_ports import ListConversationsInputPort
from lib.core.usecase_models.list_conversations_usecase_models import (
    ListConversationsError,
    ListConversationsRequest,
    ListConversationsResponse,
)


class ListConversationsUseCase(ListConversationsInputPort):
    def execute(self, request: ListConversationsRequest) -> ListConversationsResponse | ListConversationsError:
        research_context_id = request.research_context_id
        dto: ListResearchContextConversationsDTO = self.research_context_repository.list_conversations(
            research_context_id=research_context_id
        )
        if dto.status:
            return ListConversationsResponse(research_context_id=research_context_id, conversations=dto.data)
        return ListConversationsError(
            research_context_id=research_context_id,
            errorType=dto.errorType,
            errorCode=dto.errorCode,
            errorMessage=dto.errorMessage,
            errorName=dto.errorName,
        )
