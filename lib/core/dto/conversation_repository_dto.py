from typing import List

from lib.core.sdk.dto import BaseDTO
from lib.core.entity.models import Conversation, ResearchContext, SourceData, TMessageBase


class ConversationDTO(BaseDTO[Conversation]):
    """
    Basic DTO for conversations

    @param conversation_id: The id of the conversation
    @type conversation_id: int | None
    @param data: The conversation to be created
    @type data: Conversation | List[Conversation] | None | List[None]
    """

    conversation_id: int | None = None


class GetConversationResearchContextDTO(BaseDTO[ResearchContext]):
    """
    DTO for a research context obtained from a conversation

    @param data: The research context of the conversation
    @type data: ResearchContext | None
    """

    data: ResearchContext | None = None


class ListConversationMessagesDTO(BaseDTO[TMessageBase]):
    """
    DTO for listing messages from a conversation

    @param data: The messages of the conversation
    @type data: List[TMessageBase] | List[None] | None
    """

    data: List[TMessageBase] | List[None] | None = None


class ListConversationSourcesDTO(BaseDTO[SourceData]):
    """
    A DTO for listing the data sources of the research context of a conversation

    @param source_data: The source data of the research context of the conversation
    @type source_data: List[SourceData] | None
    """

    data: List[SourceData] | None = None
