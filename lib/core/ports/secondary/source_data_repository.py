from abc import ABC, abstractmethod
import logging

from lib.core.dto.source_data_repository_dto import ListSourceDataDTO


class SourceDataRepositoryOutputPort(ABC):
    """
    Abstract base class for the source data repository output port.

    @cvar logger: The logger for this class
    @type logger: logging.Logger
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @abstractmethod
    def list_source_data(self, knowledge_source_id: int | None = None) -> ListSourceDataDTO:
        """
        Lists source data. If a knowledge source ID is provided, only source data for that knowledge source will be listed, otherwise all source data will be listed.

        @param knowledge_source_id: The ID of the knowledge source to list the source data for.
        @type knowledge_source_id: int
        @return: A DTO containing the result of the operation.
        @rtype: ListSourceDataDTO
        """
        raise NotImplementedError
