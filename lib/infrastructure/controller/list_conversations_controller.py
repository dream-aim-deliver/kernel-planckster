from fastapi import HTTPException
from pydantic import Field
from lib.core.sdk.controller import BaseController, BaseControllerParameters
from lib.core.usecase.list_conversations_usecase import ListConversationsUseCase
from lib.core.usecase_models.list_conversations_usecase_models import (
    ListConversationsError,
    ListConversationsRequest,
    ListConversationsResponse,
)
from lib.core.view_model.list_conversations_view_model import ListConversationsViewModel
from lib.infrastructure.presenter.list_conversations_presenter import ListConversationsPresenter


class ListConversationsControllerParameters(BaseControllerParameters):
    research_context_id: int = Field(
        name="Reseach Context ID", description="Research context id for which the conversations are to be listed."
    )


class ListConversationsController(
    BaseController[
        ListConversationsControllerParameters,
        ListConversationsRequest,
        ListConversationsResponse,
        ListConversationsError,
        ListConversationsViewModel,
    ]
):
    def __init__(self, usecase: ListConversationsUseCase, presenter: ListConversationsPresenter) -> None:
        super().__init__(usecase=usecase, presenter=presenter)

    def create_request(self, parameters: ListConversationsControllerParameters | None) -> ListConversationsRequest:
        if parameters is None:
            raise HTTPException(status_code=400, detail="Invalid request parameters.")
        else:
            return ListConversationsRequest(research_context_id=parameters.research_context_id)
