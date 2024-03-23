from fastapi import HTTPException
from pydantic import Field
from lib.core.sdk.controller import BaseController, BaseControllerParameters
from lib.core.usecase.list_messages_usecase import ListMessagesUseCase
from lib.core.usecase_models.list_messages_usecase_models import (
    ListMessagesError,
    ListMessagesRequest,
    ListMessagesResponse,
)
from lib.core.view_model.list_messages_view_model import ListMessagesViewModel
from lib.infrastructure.presenter.list_messages_presenter import ListMessagesPresenter


class ListMessagesControllerParameters(BaseControllerParameters):
    conversation_id: int = Field(
        title="Conversation ID",
        description="Conversation ID for which the messages are to be listed.",
    )


class ListMessagesController(
    BaseController[
        ListMessagesControllerParameters,
        ListMessagesRequest,
        ListMessagesResponse,
        ListMessagesError,
        ListMessagesViewModel,
    ]
):
    def __init__(self, usecase: ListMessagesUseCase, presenter: ListMessagesPresenter) -> None:
        super().__init__(usecase=usecase, presenter=presenter)

    def create_request(self, parameters: ListMessagesControllerParameters | None) -> ListMessagesRequest:
        if parameters is None:
            raise HTTPException(status_code=400, detail="Invalid request parameters.")

        else:
            return ListMessagesRequest(conversation_id=parameters.conversation_id)
