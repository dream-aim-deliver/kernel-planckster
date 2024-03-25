from lib.core.dto.client_repository_dto import ListResearchContextsDTO
from lib.core.ports.primary.list_research_contexts_primary_ports import ListResearchContextsInputPort
from lib.core.usecase_models.list_research_contexts_usecase_models import (
    ListResearchContextsError,
    ListResearchContextsRequest,
    ListResearchContextsResponse,
)


class ListResearchContextsUseCase(ListResearchContextsInputPort):
    def execute(self, request: ListResearchContextsRequest) -> ListResearchContextsResponse | ListResearchContextsError:
        client_id = request.client_id

        dto_core_research_contexts: ListResearchContextsDTO = self.client_repository.list_research_contexts(
            client_id=client_id
        )

        if not dto_core_research_contexts.status:
            return ListResearchContextsError(
                client_id=client_id,
                errorType=dto_core_research_contexts.errorType,
                errorCode=dto_core_research_contexts.errorCode,
                errorMessage=dto_core_research_contexts.errorMessage,
                errorName=dto_core_research_contexts.errorName,
            )

        return ListResearchContextsResponse(client_id=client_id, research_contexts=dto_core_research_contexts.data)
