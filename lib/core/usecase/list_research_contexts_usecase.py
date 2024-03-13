from lib.core.dto.user_repository_dto import ListUserResearchContextsDTO
from lib.core.ports.primary.list_research_contexts_primary_ports import ListResearchContextsInputPort
from lib.core.usecase_models.list_research_contexts_usecase_models import (
    ListResearchContextsError,
    ListResearchContextsRequest,
    ListResearchContextsResponse,
)


class ListResearchContextsUseCase(ListResearchContextsInputPort):
    def execute(self, request: ListResearchContextsRequest) -> ListResearchContextsResponse | ListResearchContextsError:
        user_id = request.user_id

        dto_core_research_contexts: ListUserResearchContextsDTO = self.user_repository.list_research_contexts(
            user_id=user_id
        )

        if not dto_core_research_contexts.status:
            return ListResearchContextsError(
                user_id=user_id,
                errorType=dto_core_research_contexts.errorType,
                errorCode=dto_core_research_contexts.errorCode,
                errorMessage=dto_core_research_contexts.errorMessage,
                errorName=dto_core_research_contexts.errorName,
            )

        return ListResearchContextsResponse(user_id=user_id, research_contexts=dto_core_research_contexts.data)
