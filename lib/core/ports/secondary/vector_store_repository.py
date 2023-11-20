from abc import ABC, abstractmethod
import logging


class VectorStoreRepositoryOutputPort(ABC):
    """
    Abstract base class for the vector store repository output port.

    @cvar logger: The logger for this class
    @type logger: logging.Logger
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def logger(self) -> logging.Logger:
        return self._logger
