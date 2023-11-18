from abc import ABC, abstractmethod
import logging
from typing import List

from lib.core.dto.user_repository_dto import GetUserDTO, ListUserResearchContextsDTO, NewUserResearchContextDTO
from lib.core.entity.models import SourceData, VectorStore


class UserRepositoryOutputPort(ABC):
    """
    Abstract base class for the user repository.

    @cvar logger: The logger for this class
    @type logger: logging.Logger
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @abstractmethod
    def get_user(self, user_id: int) -> GetUserDTO:
        """
        Gets a user by ID.

        @param user_id: The ID of the user to get.
        @type user_id: int
        @return: A DTO containing the result of the operation.
        @rtype: GetUserDTO
        """
        raise NotImplementedError

    @abstractmethod
    def new_research_context(
        self, research_context_title: str, user_id: int, llm_id: int, source_data_ids: List[int]
    ) -> NewUserResearchContextDTO:
        """
        Creates a new research context for a user.

        @param research_context_title: The title of the research context.
        @type research_context_title: str
        @param user_id: The ID of the user to create the research context for.
        @type user_id: int
        @param llm_id: The ID of the LLM tied to the research context.
        @type llm_id: int
        @param source_data: The source data tied to the research context.
        @type source_data: List[SourceData]
        @param vector_store: The vector store tied to the research context.
        @type vector_store: VectorStore
        @return: A DTO containing the result of the operation.
        @rtype: NewUserResearchContextDTO
        """
        raise NotImplementedError

    @abstractmethod
    def list_research_contexts(self, user_id: int) -> ListUserResearchContextsDTO:
        """
        Lists all research contexts for a user.

        @param user_id: The ID of the user to list research contexts for.
        @type user_id: int
        @return: A DTO containing the result of the operation.
        @rtype: ListUserResearchContextsDTO
        """
        raise NotImplementedError
