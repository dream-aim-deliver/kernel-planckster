from typing import List

from lib.core.sdk.dto import BaseDTO
from lib.core.entity.models import Conversation, ResearchContext, SourceData, TMessageBase


class ConversationDTO(BaseDTO[Conversation]):
    """
    Basic DTO for conversations

    @param data: The conversation to be created
    @type data: Conversation | List[Conversation] | None | List[None]
    """

    pass


class GetConversationResearchContextDTO(BaseDTO[ResearchContext]):
    """
    DTO for a research context obtained from a conversation

    @param data: The research context of the conversation
    @type data: ResearchContext
    """

    data: ResearchContext | None = None


class ListConversationMessagesDTO(BaseDTO[TMessageBase]):
    """
    DTO for listing messages from a conversation

    @param data: The messages of the conversation
    @type data: List[TMessageBase] | List[None]
    """

    data: List[TMessageBase] | List[None] | None = None


class ListConversationsDTO(BaseDTO[Conversation]):
    """
    DTO for listing conversations from a research context

    @param data: The conversations to be listed
    @type data: List[Conversation] | List[None]
    """

    data: List[Conversation] | List[None] | None = None


class ListConversationSourcesDTO(BaseDTO[SourceData]):
    """
    A DTO for listing the data sources of the research context of a conversation

    @param source_data: The source data of the research context of the conversation
    @type source_data: List[SourceData] | List[None]
    """

    # TODO: are we allowing research contexts without source data?
    data: List[SourceData] | List[None] | None = None
