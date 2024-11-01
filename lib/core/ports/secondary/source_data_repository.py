from abc import ABC, abstractmethod
import logging
from typing import Any, Generic

from lib.core.sdk.repository import TSession
from lib.core.dto.source_data_repository_dto import GetSourceDataByProtocolRelativePathDTO
from lib.core.entity.models import ProtocolEnum


class SourceDataRepositoryOutputPort(ABC, Generic[TSession]):
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
    def get_source_data_by_composite_index(
        self,
        session: TSession,
        client_id: int,
        protocol: ProtocolEnum,
        relative_path: str,
    ) -> GetSourceDataByProtocolRelativePathDTO:
        """
        Gets source data by its composite index.

        @param session: An open session provided by the context manager.
        @type session: TSession
        @param client_id: The ID of the client that owns the source data.
        @type client_id: int
        @param protocol: The protocol of the source data.
        @type protocol: ProtocolEnum
        @param relative_path: The relative path of the source data.
        @type relative_path: str
        @return: A DTO containing the result of the operation.
        @rtype: GetSourceDataByLFNDTO
        """
        raise NotImplementedError
