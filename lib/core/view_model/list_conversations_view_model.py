from typing import List

from pydantic import Field
from lib.core.entity.models import Conversation
from lib.core.sdk.viewmodel import BaseViewModel


class ListConversationsViewModel(BaseViewModel):
    """
    View Model for the List Conversations Feature. Represents all conversations in a given research context.
    """

    research_context_id: int = Field(description="Research context id for which the conversations are to be listed.")
    conversations: List[Conversation] = Field(description="List of conversations in the research context.")
