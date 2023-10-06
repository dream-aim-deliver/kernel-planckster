from abc import ABC, abstractmethod
import logging
from typing import List

from lib.core.dto.conversation_repository_dto import (
    SuccessConversationDTO,
    ErrorConversationDTO,
    GetConversationDTO,
    ListConversationsDTO,
    ListConversationSourcesDTO,
)
from lib.core.entity.models import TMessageBase


class ConversationRepository(ABC):
    """
    Abstract base class for conversation repositories.

    @cvar logger: The logger for this class.
    @type logger: logging.Logger
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def new_conversation(self, research_context_id: int) -> SuccessConversationDTO | ErrorConversationDTO:
        """
        Creates a new conversation in the research context.

        @param research_context_id: The ID of the research context to create the conversation in.
        @type research_context_id: int
        @return: A DTO containing the result of the operation.
        @rtype: SuccessConversationDTO | ErrorConversationDTO
        """
        raise NotImplementedError

    @abstractmethod
    def get_conversation(self, conversation_id: int) -> GetConversationDTO[TMessageBase] | ErrorConversationDTO:
        """
        Displays information about a conversation in the research context.

        @param conversation_id: The ID of the conversation to display.
        @type conversation_id: int
        @return: A DTO containing the result of the operation.
        @rtype: GetConversationDTO[TMessageBase] | ErrorConversationDTO
        """
        raise NotImplementedError

    @abstractmethod
    def update_conversation(
        self,
        conversation_id: int,
        conversation_title: str,  # TODO: are we allowing changing titles?
        messages: List[TMessageBase]
        | List[None],  # TODO: are we allowing updates with empty lists of messages? no, right?
    ) -> SuccessConversationDTO | ErrorConversationDTO:
        """
        Updates a conversation in the research context.

        @param conversation_id: The ID of the conversation to update.
        @type conversation_id: int
        @param conversation_title: The title of the conversation.
        @type conversation_title: str
        @param messages: The messages to add to the conversation.
        @type messages: List[TMessageBase] | List[None]
        @return: A DTO containing the result of the operation.
        @rtype: SuccessConversationDTO | ErrorConversationDTO
        """
        raise NotImplementedError

    @abstractmethod
    def list_conversations(self, research_context_id: int) -> ListConversationsDTO | ErrorConversationDTO:
        """
        Lists all conversations in the research context.

        @param research_context_id: The ID of the research context to list conversations for.
        @type research_context_id: int
        @return: A DTO containing the result of the operation.
        @rtype: ListConversationsDTO | ErrorConversationDTO
        """
        raise NotImplementedError

    @abstractmethod
    def list_conversation_sources(self, conversation_id: int) -> ListConversationSourcesDTO | ErrorConversationDTO:
        """
        Lists all data sources of the research context of a conversation.

        @param conversation_id: The ID of the conversation to list data sources for.
        @type conversation_id: int
        @return: A DTO containing the result of the operation.
        @rtype: ListConversationSourcesDTO | ErrorConversationDTO
        """
        raise NotImplementedError
