from fastapi import HTTPException
from pydantic import Field
from lib.core.sdk.controller import BaseController, BaseControllerParameters
from lib.core.usecase.new_conversation_usecase import NewConversationUseCase
from lib.core.usecase_models.new_conversation_usecase_models import (
    NewConversationError,
    NewConversationRequest,
    NewConversationResponse,
)
from lib.core.view_model.new_conversation_view_model import NewConversationViewModel
from lib.infrastructure.presenter.new_conversation_presenter import NewConversationPresenter


class NewConversationControllerParameters(BaseControllerParameters):
    research_context_id: int = Field(
        name="Research Context ID",
        description="The ID of the research context for which the conversation is to be created.",
    )
    conversation_title: str = Field(
        name="Conversation Title",
        description="Title of the conversation to be created.",
    )


class NewConversationController(
    BaseController[
        NewConversationControllerParameters,
        NewConversationRequest,
        NewConversationResponse,
        NewConversationError,
        NewConversationViewModel,
    ]
):
    def __init__(
        self,
        usecase: NewConversationUseCase,
        presenter: NewConversationPresenter,
    ) -> None:
        super().__init__(usecase=usecase, presenter=presenter)

    def create_request(self, parameters: NewConversationControllerParameters | None) -> NewConversationRequest:
        if parameters is None:
            raise HTTPException(status_code=400, detail="Invalid request parameters.")
        else:
            return NewConversationRequest(
                research_context_id=parameters.research_context_id, conversation_title=parameters.conversation_title
            )
