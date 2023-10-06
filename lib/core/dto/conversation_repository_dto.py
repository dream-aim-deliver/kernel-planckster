from typing import Generic, Literal, List

from lib.core.sdk.dto import BaseDTO
from lib.core.entity.models import Conversation, SourceData, TMessageBase


class SuccessConversationDTO(BaseDTO):
    """
    Successful DTO for conversations

    @param status: The status of the operation
    @type status: Literal["success"]
    """

    status: Literal["success"]


class ErrorConversationDTO(BaseDTO):
    """
    Error DTO for conversations

    @param status: The status of the operation
    @type status: Literal["error"]
    """

    status: Literal["error"]


class GetConversationDTO(BaseDTO, Conversation, Generic[TMessageBase]):
    """
    Successful DTO for conversations

    @param status: The status of the operation
    @type status: Literal["success"]
    @param messages: The messages of the conversation
    @type messages: List[TMessageBase] | List[None]
    """

    status: Literal["success"]
    messages: List[TMessageBase] | List[None]


class ListConversationsDTO(BaseDTO):
    """
    DTO for listing conversations

    @param status: The status of the operation
    @type status: Literal["success"]
    @param notes: The notes of the conversation
    @type notes: List[Conversation] | List[None]
    """

    status: Literal["success"]
    notes: List[Conversation] | List[None]


class ListConversationSourcesDTO(BaseDTO):
    """
    A DTO for listing the data sources of the research context of a conversation

    @param status: The status of the operation
    @type status: Literal["success"]
    @param source_data: The source data of the research context of the conversation
    @type source_data: List[SourceData] | List[None]
    """

    status: Literal["success"]
    source_data: List[SourceData] | List[None]  # TODO: are we allowing research contexts without source data?
