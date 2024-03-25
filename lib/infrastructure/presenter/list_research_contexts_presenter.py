from lib.core.ports.primary.list_research_contexts_primary_ports import ListResearchContextsOutputPort
from lib.core.usecase_models.list_research_contexts_usecase_models import (
    ListResearchContextsError,
    ListResearchContextsResponse,
)
from lib.core.view_model.list_research_contexts_view_model import ListResearchContextsViewModel


class ListResearchContextsPresenter(ListResearchContextsOutputPort):
    def convert_error_response_to_view_model(
        self, response: ListResearchContextsError
    ) -> ListResearchContextsViewModel:
        return ListResearchContextsViewModel(
            status=False,
            research_contexts=[],
            client_id=response.client_id,
            code=response.errorCode,
            errorCode=response.errorCode,
            errorMessage=response.errorMessage,
            errorName=response.errorName,
            errorType=response.errorType,
        )

    def convert_response_to_view_model(self, response: ListResearchContextsResponse) -> ListResearchContextsViewModel:
        return ListResearchContextsViewModel(
            status=True,
            client_id=response.client_id,
            research_contexts=response.research_contexts,
            code=200,
        )
