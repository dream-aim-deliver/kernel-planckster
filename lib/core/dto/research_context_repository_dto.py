from typing import List
from lib.core.entity.models import Conversation
from lib.core.sdk.dto import BaseDTO


class ListResearchContextConversations(BaseDTO[Conversation]):
    """
    A DTO for listing all conversations in a research context

    @param data: The conversations in the research context
    """

    data: List[Conversation] | None = None
