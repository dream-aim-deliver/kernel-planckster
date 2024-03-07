from pydantic import Field
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest, BaseResponse


class NewConversationRequest(BaseRequest):
    """
    Request model for the New Conversation Use Case.

    @param research_context_id: The ID of the research context for which the conversation is to be created.
    @param conversation_title: Title of the conversation to be created.
    """

    research_context_id: int = Field(
        description="The ID of the research context for which the conversation is to be created."
    )
    conversation_title: str = Field(description="Title of the conversation to be created.")


class NewConversationResponse(BaseResponse):
    """
    Response model for the New Conversation Use Case.

    @param conversation_id: The ID of the newly created conversation.
    """

    conversation_id: int = Field(description="The ID of the newly created conversation.")


class NewConversationError(BaseErrorResponse):
    """
    Error response model for the New Conversation Use Case.
    """

    pass
