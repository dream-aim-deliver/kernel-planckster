from fastapi import HTTPException
from pydantic import Field
from lib.core.sdk.controller import BaseController, BaseControllerParameters
from lib.core.usecase.list_source_data_for_research_context_usecase import ListSourceDataForResearchContextUseCase
from lib.core.usecase_models.list_source_data_for_research_context_usecase_models import (
    ListSourceDataForResearchContextError,
    ListSourceDataForResearchContextRequest,
    ListSourceDataForResearchContextResponse,
)
from lib.core.view_model.list_source_data_for_research_context_view_model import (
    ListSourceDataForResearchContextViewModel,
)
from lib.infrastructure.presenter.list_source_data_for_research_context_presenter import (
    ListSourceDataForResearchContextPresenter,
)


class ListSourceDataForResearchContextControllerParameters(BaseControllerParameters):
    research_context_id: int = Field(
        name="Research Context ID",
        description="Research Context ID for which the source data is to be listed.",
    )


class ListSourceDataForResearchContextController(
    BaseController[
        ListSourceDataForResearchContextControllerParameters,
        ListSourceDataForResearchContextRequest,
        ListSourceDataForResearchContextResponse,
        ListSourceDataForResearchContextError,
        ListSourceDataForResearchContextViewModel,
    ]
):
    def __init__(
        self, usecase: ListSourceDataForResearchContextUseCase, presenter: ListSourceDataForResearchContextPresenter
    ) -> None:
        super().__init__(usecase=usecase, presenter=presenter)

    def create_request(
        self, parameters: ListSourceDataForResearchContextControllerParameters | None
    ) -> ListSourceDataForResearchContextRequest:
        if parameters is None:
            raise HTTPException(status_code=400, detail="Invalid request parameters.")

        else:
            return ListSourceDataForResearchContextRequest(research_context_id=parameters.research_context_id)
