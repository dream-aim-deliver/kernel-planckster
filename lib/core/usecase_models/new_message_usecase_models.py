from typing import List
from pydantic import Field
from lib.core.entity.models import MessageSenderTypeEnum
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest, BaseResponse


class NewMessageRequest(BaseRequest):
    """
    Request model for the New Message Use Case.

    @param conversation_id: The ID of the conversation to which the message is to be added.
    @param message_content: The content of the message to be added.
    @param sender_type: The type of the sender of the message. Can be either 'user' or 'agent'.
    @param timestamp: The timestamp of the message. Needs to be a valid unix timestamp.
    """

    conversation_id: int = Field(description="The ID of the conversation to which the message is to be added.")
    message_contents: List[str] = Field(description="The contents of the message to be added.")
    sender_type: str = Field(description="The type of the sender of the message. Can be either 'user' or 'agent'.")
    unix_timestamp: int = Field(description="The timestamp of the message. Needs to be a valid timestamp in Unix time.")
    thread_id: int | None = Field(
        description="The ID of the thread to which the message belongs. Only passed when message is in response to an existing message."
    )


class NewMessageResponse(BaseResponse):
    """
    Response model for the New Message Use Case.

    @param id: The ID of the newly created message.
    """

    message_id: int = Field(description="The ID of the newly created message.")


class NewMessageError(BaseErrorResponse):
    """
    Error response model for the New Message Use Case.
    """

    pass
