from lib.core.ports.primary.list_source_data_for_research_context_primary_ports import (
    ListSourceDataForResearchContextOutputPort,
)
from lib.core.usecase_models.list_source_data_for_research_context_usecase_models import (
    ListSourceDataForResearchContextError,
    ListSourceDataForResearchContextResponse,
)
from lib.core.view_model.list_source_data_for_research_context_view_model import (
    ListSourceDataForResearchContextViewModel,
)


class ListSourceDataForResearchContextPresenter(ListSourceDataForResearchContextOutputPort):
    def convert_error_response_to_view_model(
        self, response: ListSourceDataForResearchContextError
    ) -> ListSourceDataForResearchContextViewModel:
        return ListSourceDataForResearchContextViewModel(
            status=False,
            source_data_list=[],
            code=response.errorCode,
            errorCode=response.errorCode,
            errorMessage=response.errorMessage,
            errorName=response.errorName,
            errorType=response.errorType,
        )

    def convert_response_to_view_model(
        self, response: ListSourceDataForResearchContextResponse
    ) -> ListSourceDataForResearchContextViewModel:
        return ListSourceDataForResearchContextViewModel(
            status=True,
            code=200,
            source_data_list=response.source_data_list,
        )
