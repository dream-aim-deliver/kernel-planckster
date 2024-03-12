from lib.core.dto.user_repository_dto import NewResearchContextDTO
from lib.core.ports.primary.new_research_context_primary_ports import NewResearchContextInputPort
from lib.core.usecase_models.new_research_context_usecase_models import (
    NewResearchContextError,
    NewResearchContextRequest,
    NewResearchContextResponse,
)


class NewResearchContextUseCase(NewResearchContextInputPort):
    def execute(self, request: NewResearchContextRequest) -> NewResearchContextResponse | NewResearchContextError:
        research_context_title = request.research_context_title
        research_context_description = request.research_context_description
        user_sid = request.user_sid
        llm_name = request.llm_name
        source_data_ids = request.source_data_ids

        dto: NewResearchContextDTO = self.user_repository.new_research_context(
            research_context_title=research_context_title,
            research_context_description=research_context_description,
            user_sid=user_sid,
            llm_name=llm_name,
            source_data_ids=source_data_ids,
        )

        if dto.status:
            return NewResearchContextResponse(research_context=dto.research_context, llm=dto.llm)

        return NewResearchContextError(
            errorCode=dto.errorCode,
            errorMessage=dto.errorMessage,
            errorName=dto.errorName,
            errorType=dto.errorType,
        )
