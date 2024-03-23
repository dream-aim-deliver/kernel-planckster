from fastapi import HTTPException
from pydantic import Field
from lib.core.sdk.controller import BaseController, BaseControllerParameters
from lib.core.usecase.new_message_usecase import NewMessageUseCase
from lib.core.usecase_models.new_message_usecase_models import NewMessageError, NewMessageRequest, NewMessageResponse
from lib.core.view_model.new_message_view_model import NewMessageViewModel
from lib.infrastructure.presenter.new_message_presenter import NewMessagePresenter


class NewMessageControllerParameters(BaseControllerParameters):
    conversation_id: int = Field(
        title="Conversation ID",
        description="The ID of the conversation to which the message is to be added.",
    )

    message_content: str = Field(
        title="Message Content",
        description="The content of the message to be added.",
    )

    sender_type: str = Field(
        title="Sender Type",
        description="The type of the sender of the message. Can be either 'user' or 'agent'.",
    )

    unix_timestamp: int = Field(
        title="Unix Timestamp",
        description="The timestamp of the message. Needs to be a valid timestamp in Unix time.",
    )


class NewMessageController(
    BaseController[
        NewMessageControllerParameters,
        NewMessageRequest,
        NewMessageResponse,
        NewMessageError,
        NewMessageViewModel,
    ]
):
    def __init__(
        self,
        usecase: NewMessageUseCase,
        presenter: NewMessagePresenter,
    ) -> None:
        super().__init__(usecase=usecase, presenter=presenter)

    def create_request(self, parameters: NewMessageControllerParameters | None) -> NewMessageRequest:
        if parameters is None:
            raise HTTPException(status_code=400, detail="Invalid request parameters.")
        else:
            return NewMessageRequest(
                conversation_id=parameters.conversation_id,
                message_content=parameters.message_content,
                sender_type=parameters.sender_type,
                unix_timestamp=parameters.unix_timestamp,
            )
