from typing import List
from lib.core.entity.models import Conversation, ResearchContext, SourceData, Client
from lib.core.sdk.dto import BaseDTO


class GetResearchContextDTO(BaseDTO[ResearchContext]):
    """
    A DTO for getting a research context

    @param data: The research context
    """

    data: ResearchContext | None = None


class GetResearchContextClientDTO(BaseDTO[Client]):
    """
    A DTO for getting the client that created a research context

    @param data: The client that created the research context
    @type data: Client | None
    """

    data: Client | None = None


class NewResearchContextConversationDTO(BaseDTO[Conversation]):
    """
    Basic DTO for conversations

    @param conversation_id: The id of the new conversation
    @type conversation_id: int | None
    """

    conversation_id: int | None = None


class ListResearchContextConversationsDTO(BaseDTO[Conversation]):
    """
    A DTO for listing all conversations in a research context

    @param data: The conversations in the research context
    """

    data: List[Conversation] | None = None


class ListSourceDataDTO(BaseDTO[SourceData]):
    """
    A DTO for listing all source data in a research context

    @param data: The source data in the research context
    """

    data: List[SourceData] | None = None
