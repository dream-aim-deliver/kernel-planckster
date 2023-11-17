from typing import List
from pydantic import Field
from lib.core.entity.models import Conversation
from lib.core.sdk.usecase_models import BaseRequest, BaseResponse


class ListConversationsRequest(BaseRequest):
    """
    Request Model for the List Conversations Use Case.
    """

    research_context_id: int = Field(description="Research context id for which the conversations are to be listed.")


class ListConversationsResponse(BaseResponse):
    """
    Response Model for the List Conversations Use Case.
    """

    data: List[Conversation] = Field(description="List of conversations in the research context.")
