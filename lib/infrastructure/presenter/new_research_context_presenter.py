from lib.core.ports.primary.new_research_context_primary_ports import NewResearchContextOutputPort
from lib.core.usecase_models.new_research_context_usecase_models import (
    NewResearchContextError,
    NewResearchContextResponse,
)
from lib.core.view_model.new_research_context_view_mode import NewResearchContextViewModel


class NewResearchContextPresenter(NewResearchContextOutputPort):
    def convert_error_response_to_view_model(self, response: NewResearchContextError) -> NewResearchContextViewModel:
        return NewResearchContextViewModel(
            status=False,
            code=response.errorCode,
            errorCode=response.errorCode,
            errorMessage=response.errorMessage,
            errorName=response.errorName,
            errorType=response.errorType,
            research_context_id=-1,
            research_context_title="",
            research_context_description="",
            llm_name="",
        )

    def convert_response_to_view_model(self, response: NewResearchContextResponse) -> NewResearchContextViewModel:
        research_context_id = response.research_context.id
        research_context_title = response.research_context.title
        llm_name = response.llm.llm_name

        return NewResearchContextViewModel(
            status=True,
            code=200,
            research_context_id=research_context_id,
            research_context_title=research_context_title,
            research_context_description=response.research_context.description,
            llm_name=llm_name,
        )
