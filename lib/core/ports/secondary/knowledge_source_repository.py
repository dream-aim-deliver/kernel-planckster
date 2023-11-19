from abc import ABC, abstractmethod
import logging
from typing import List
from lib.core.dto.knowledge_source_repository_dto import NewSourceDataDTO

from lib.core.entity.models import SourceData


class KnowledgeSourceRepositoryOutputPort(ABC):
    """
    Abstract base class for the knowledge source repository.

    @cvar logger: The logger for this class
    @type logger: logging.Logger
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @abstractmethod
    def new_source_data(self, knowledge_source_id: int, source_data_list: List[SourceData]) -> NewSourceDataDTO:
        """
        Creates a new source data.

        @param knowledge_source_id: The ID of the knowledge source to create the source data for.
        @type knowledge_source_id: int
        @param source_data_list: The list of source data to create.
        @type source_data_list: List[SourceData]
        @return: A DTO containing the result of the operation.
        @rtype: NewSourceDataDTO
        """
        raise NotImplementedError
