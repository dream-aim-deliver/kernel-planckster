from fastapi import HTTPException
from pydantic import Field
from lib.core.sdk.controller import BaseController, BaseControllerParameters
from lib.core.usecase.list_research_contexts_usecase import ListResearchContextsUseCase
from lib.core.usecase_models.list_research_contexts_usecase_models import (
    ListResearchContextsError,
    ListResearchContextsRequest,
    ListResearchContextsResponse,
)
from lib.core.view_model.list_research_contexts_view_model import ListResearchContextsViewModel
from lib.infrastructure.presenter.list_research_contexts_presenter import ListResearchContextsPresenter


class ListResearchContextsControllerParameters(BaseControllerParameters):
    user_id: int = Field(description="User ID for which the research contexts are to be listed.")


class ListResearchContextsController(
    BaseController[
        ListResearchContextsControllerParameters,
        ListResearchContextsRequest,
        ListResearchContextsResponse,
        ListResearchContextsError,
        ListResearchContextsViewModel,
    ]
):
    def __init__(self, usecase: ListResearchContextsUseCase, presenter: ListResearchContextsPresenter) -> None:
        super().__init__(usecase=usecase, presenter=presenter)

    def create_request(
        self, parameters: ListResearchContextsControllerParameters | None
    ) -> ListResearchContextsRequest:
        if parameters is None:
            raise HTTPException(status_code=400, detail="Invalid request parameters.")
        else:
            return ListResearchContextsRequest(user_id=parameters.user_id)
