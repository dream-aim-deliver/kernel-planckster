from typing import List
from lib.core.entity.models import Conversation, ResearchContext, User, VectorStore
from lib.core.sdk.dto import BaseDTO


class GetResearchContextDTO(BaseDTO[ResearchContext]):
    """
    A DTO for getting a research context

    @param data: The research context
    """

    data: ResearchContext | None = None


class UpdateResearchContextVectorStoreDTO(BaseDTO[VectorStore]):
    """
    A DTO for updating the vector store of a research context

    @param research_context_id. The ID of the research context that was updated
    @type research_context_id: int | None = None
    @param vector_store_id: The ID of vector store that was registered for the research context
    @type vector_store_id: int | None = None
    """

    research_context_id: int | None = None
    vector_store_id: int | None = None


class GetResearchContextUserDTO(BaseDTO[User]):
    """
    A DTO for getting the user of a research context

    @param data: The user of the research context
    @type data: User | None
    """

    data: User | None = None


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
