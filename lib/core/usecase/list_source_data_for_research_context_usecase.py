from lib.core.dto.research_context_repository_dto import ListSourceDataDTO
from lib.core.ports.primary.list_source_data_for_research_context_primary_ports import (
    ListSourceDataForResearchContextInputPort,
)
from lib.core.usecase_models.list_source_data_for_research_context_usecase_models import (
    ListSourceDataForResearchContextError,
    ListSourceDataForResearchContextRequest,
    ListSourceDataForResearchContextResponse,
)


class ListSourceDataForResearchContextUseCase(ListSourceDataForResearchContextInputPort):
    def execute(
        self, request: ListSourceDataForResearchContextRequest
    ) -> ListSourceDataForResearchContextResponse | ListSourceDataForResearchContextError:
        research_context_id = request.research_context_id

        dto: ListSourceDataDTO = self.research_context_repository.list_source_data(
            research_context_id=research_context_id
        )

        if dto.status:
            return ListSourceDataForResearchContextResponse(source_data_list=dto.data)

        return ListSourceDataForResearchContextError(
            research_context_id=research_context_id,
            errorCode=dto.errorCode,
            errorMessage=dto.errorMessage,
            errorName=dto.errorName,
            errorType=dto.errorType,
        )
