from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import List
from lib.core.entity.models import BaseMessageContent, MessageContentTypeEnum
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

    message_contents: List[BaseMessageContent] = Field(
        title="Message Contents",
        description="The pieces of content connected to the new message.",
    )

    sender_type: str = Field(
        title="Sender Type",
        description="The type of the sender of the message. Can be either 'user' or 'agent'.",
    )

    unix_timestamp: int = Field(
        title="Unix Timestamp",
        description="The timestamp of the message. Needs to be a valid timestamp in Unix time.",
    )

    thread_id: int | None = Field(
        title="Thread ID",
        description="The ID of the thread to which the message belongs. Only passed when message is in response to an existing message.",
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
                message_contents=parameters.message_contents,
                sender_type=parameters.sender_type,
                unix_timestamp=parameters.unix_timestamp,
                thread_id=parameters.thread_id,
            )
