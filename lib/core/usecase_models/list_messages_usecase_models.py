from typing import List
from lib.core.entity.models import MessageBase
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest, BaseResponse


class ListMessagesRequest(BaseRequest):
    """
    Request Model for the List Messages Use Case.
    """

    conversation_id: int


class ListMessagesResponse(BaseResponse):
    """
    Response Model for the List Messages Use Case.
    """

    message_list: List[MessageBase]


class ListMessagesError(BaseErrorResponse):
    """
    Error Response Model for the List Messages Use Case.
    """

    conversation_id: int
