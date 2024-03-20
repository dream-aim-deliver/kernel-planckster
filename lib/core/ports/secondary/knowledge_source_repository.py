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
    def new_source_data(self, knowledge_source_id: int, source_data: SourceData) -> NewSourceDataDTO:
        """
        Registers a new source data in the database.

        @param knowledge_source_id: The ID of the knowledge source to create the source data for.
        @type knowledge_source_id: int
        @param source_data: The source data to register.
        @type source_data: SourceData
        @return: A DTO containing the result of the operation.
        @rtype: NewSourceDataDTO
        """
        raise NotImplementedError
