from abc import ABC, abstractmethod
import logging
from typing import List

from lib.core.dto.client_repository_dto import (
    GetClientDTO,
    ListResearchContextsDTO,
    ListSourceDataDTO,
    NewResearchContextDTO,
    NewSourceDataDTO,
)
from lib.core.entity.models import ProtocolEnum


class ClientRepositoryOutputPort(ABC):
    """
    Abstract base class for the client repository.

    @cvar logger: The logger for this class
    @type logger: logging.Logger
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @abstractmethod
    def get_client(self, client_id: int) -> GetClientDTO:
        """
        Gets a client by ID.

        @param client_id: The ID of the client to get.
        @type client_id: int
        @return: A DTO containing the result of the operation.
        @rtype: GetClientDTO
        """
        raise NotImplementedError

    @abstractmethod
    def get_client_by_sub(self, client_sub: str) -> GetClientDTO:
        """
        Gets a client by SUB.

        @param client_sub: The SUB of the client to get.
        @type client_sub: str
        @return: A DTO containing the result of the operation.
        @rtype: GetClientDTO
        """
        raise NotImplementedError

    @abstractmethod
    def new_research_context(
        self,
        research_context_title: str,
        research_context_description: str,
        client_sub: str,
        llm_name: str,
        external_id: str,
        source_data_ids: List[int],
    ) -> NewResearchContextDTO:
        """
        Creates a new research context for a client.

        @param research_context_title: The title of the research context.
        @type research_context_title: str
        @param research_context_description: The description of the research context.
        @type research_context_description: str
        @param client_sub: The SUB of the client to create the research context for.
        @type client_sub: str
        @param llm_name: The name of the LLM to create the research context for.
        @type llm_name: str
        @param source_data_ids: The IDs of the source data to create the research context for.
        @type source_data_ids: List[int]
        @param external_id: The UUID that is used to trace vector stores and agents in the externally managed databases.
        @type external_id: str
        @return: A DTO containing the result of the operation.
        @rtype: NewResearchContextDTO
        """
        raise NotImplementedError

    @abstractmethod
    def list_research_contexts(self, client_id: int) -> ListResearchContextsDTO:
        """
        Lists all research contexts for a client.

        @param client_id: The ID of the client to list research contexts for.
        @type client_id: int
        @return: A DTO containing the result of the operation.
        @rtype: ListResearchContextsDTO
        """
        raise NotImplementedError

    @abstractmethod
    def new_source_data(
        self, client_id: int, source_data_name: str, protocol: ProtocolEnum, relative_path: str
    ) -> NewSourceDataDTO:
        """
        Registers a new source data in the database for a given client.

        @param client_id: The ID of the client to create the source data for.
        @type client_id: int
        @param source_data_name: The name of the source data.
        @type source_data_name: str
        @param protocol: The protocol of the source data.
        @type protocol: ProtocolEnum
        @param relative_path: The relative path of the source data.
        @type relative_path: str
        @return: A DTO containing the result of the operation.
        @rtype: NewSourceDataDTO
        """
        raise NotImplementedError

    @abstractmethod
    def list_source_data(self, client_id: int) -> ListSourceDataDTO:
        """
        Lists source data for a given client.

        @param client_id: The ID of the client to list the source data for.
        @type client_id: int
        @return: A DTO containing the result of the operation.
        @rtype: ListSourceDataDTO
        """
        raise NotImplementedError
