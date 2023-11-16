from abc import ABC, abstractmethod
import logging
from typing import List

from lib.core.dto.conversation_repository_dto import (
    ConversationDTO,
    GetConversationResearchContextDTO,
    ListConversationMessagesDTO,
    ListConversationSourcesDTO,
    ListConversationsDTO,
)
from lib.core.entity.models import TMessageBase


class ConversationRepository(ABC):
    """
    Abstract base class for the conversation repository.

    @cvar logger: The logger for this class
    @type logger: logging.Logger
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def new_conversation(self, research_context_id: int, conversation_title: str) -> ConversationDTO:
        """
        Creates a new conversation in the research context.

        @param research_context_id: The ID of the research context to create the conversation in.
        @type research_context_id: int
        @param conversation_title: The title of the conversation.
        @type conversation_title: str
        @return: A DTO containing the result of the operation.
        @rtype: ConversationDTO
        """
        raise NotImplementedError

    @abstractmethod
    def get_conversation_research_context(self, conversation_id: int) -> GetConversationResearchContextDTO:
        """
        Gets the research context of a conversation.

        @param research_context_id: The ID of the research context to get the conversation for.
        @type research_context_id: int
        @return: A DTO containing the result of the operation.
        @rtype: GetConversationResearchContextDTO
        """
        raise NotImplementedError

    @abstractmethod
    def list_conversation_messages(self, conversation_id: int) -> ListConversationMessagesDTO[TMessageBase]:
        """
        Lists all messages in a conversation.

        @param conversation_id: The ID of the conversation to list messages for.
        @type conversation_id: int
        @return: A DTO containing the result of the operation.
        """
        raise NotImplementedError

    @abstractmethod
    def update_conversation(self, conversation_id: int, conversation_title: str) -> ConversationDTO:
        """
        Updates a conversation in the research context.

        @param conversation_id: The ID of the conversation to update.
        @type conversation_id: int
        @param conversation_title: The title of the conversation.
        @type conversation_title: str
        @return: A DTO containing the result of the operation.
        @rtype: ConversationDTO
        """
        raise NotImplementedError

    @abstractmethod
    def list_conversation_sources(self, conversation_id: int) -> ListConversationSourcesDTO:
        """
        Lists all data sources of the citations of a conversation.

        @param conversation_id: The ID of the conversation to list data sources for.
        @type conversation_id: int
        @return: A DTO containing the result of the operation.
        @rtype: ListConversationSourcesDTO
        """
        raise NotImplementedError

    @abstractmethod
    def list_conversations(self) -> ListConversationsDTO:
        """
        Lists all conversations in the database.

        @return: A DTO containing the result of the operation.
        @rtype: ListConversationsDTO
        """
        raise NotImplementedError
