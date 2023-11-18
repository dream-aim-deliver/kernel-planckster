from typing import List
from lib.core.entity.models import Conversation, ResearchContext
from lib.core.sdk.dto import BaseDTO


class GetResearchContextDTO(BaseDTO[ResearchContext]):
    """
    A DTO for getting a research context

    @param data: The research context
    """

    data: ResearchContext | None = None


class NewResearchContextConversationDTO(BaseDTO[Conversation]):
    """
    Basic DTO for conversations

    @param conversation_id: The id of the conversation
    @type conversation_id: int | None
    @param data: The conversation to be created
    @type data: Conversation | List[Conversation] | None | List[None]
    """

    conversation_id: int | None = None


class ListResearchContextConversationsDTO(BaseDTO[Conversation]):
    """
    A DTO for listing all conversations in a research context

    @param data: The conversations in the research context
    """

    data: List[Conversation] | None = None
