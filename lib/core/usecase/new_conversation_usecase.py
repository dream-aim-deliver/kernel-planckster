from lib.core.dto.research_context_repository_dto import NewResearchContextConversationDTO
from lib.core.ports.primary.new_conversation_primary_ports import NewConversationInputPort
from lib.core.usecase_models.new_conversation_usecase_models import (
    NewConversationError,
    NewConversationRequest,
    NewConversationResponse,
)


class NewConversationUseCase(NewConversationInputPort):
    def execute(self, request: NewConversationRequest) -> NewConversationResponse | NewConversationError:
        research_context_id = request.research_context_id
        conversation_title = request.conversation_title

        dto: NewResearchContextConversationDTO = self.research_context_repository.new_conversation(
            research_context_id=research_context_id, conversation_title=conversation_title
        )

        if dto.status:
            return NewConversationResponse(conversation_id=dto.conversation_id)

        return NewConversationError(
            errorCode=dto.errorCode,
            errorMessage=dto.errorMessage,
            errorName=dto.errorName,
            errorType=dto.errorType,
        )
