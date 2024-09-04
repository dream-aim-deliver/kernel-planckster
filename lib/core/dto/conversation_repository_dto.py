from typing import List

from lib.core.sdk.dto import BaseDTO
from lib.core.entity.models import (
    AgentMessage,
    Conversation,
    MessageBase,
    ResearchContext,
    SourceData,
    TMessageBase,
    UserMessage,
    MessageContent,
)


class GetConversationDTO(BaseDTO[Conversation]):
    """
    DTO for a conversation obtained by ID

    @param data: The conversation
    @type data: Conversation | None
    """

    data: Conversation | None = None


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

    data: List[TMessageBase] | None = None


class UpdateConversationDTO(BaseDTO[Conversation]):
    """
    Basic DTO for conversations

    @param conversation_id: The id of the conversation
    @type conversation_id: int | None
    @param data: The conversation to be created
    @type data: Conversation | List[Conversation] | None | List[None]
    """

    conversation_id: int | None = None


class ListConversationSourcesDTO(BaseDTO[SourceData]):
    """
    A DTO for listing the data sources of the citations of a conversation

    @param data: The source data of the citations of all of the message responses of the conversation
    @type data: List[SourceData] | None
    """

    data: List[SourceData] | None = None


class NewMessageDTO(BaseDTO[MessageBase]):
    """
    A DTO for sending a message to a conversation

    @param data: The new message registered in the conversation
    @type data: TMessageBase | None
    """

    data: UserMessage | AgentMessage | None = None

class NewMessageContentDTO(BaseDTO[MessageContent]):
    """
    A DTO for adding a piece of content to a message

    @param data: The new content to add to the message
    @type data: MessageContent | None
    """

    data: MessageContent | None = None
