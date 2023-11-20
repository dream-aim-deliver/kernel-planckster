from abc import ABC, abstractmethod
import logging
from lib.core.dto.vector_store_dto import NewVectorStoreDTO

from lib.core.entity.models import ProtocolEnum


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

    @abstractmethod
    def new_vector_store(
        self,
        vector_store_lfn: str,
        vector_store_name: str,
        vector_store_protocol: ProtocolEnum,
        embedding_model_id: int,
    ) -> NewVectorStoreDTO:
        """
        Create a new vector store.

        @param vector_store_lfn: The LFN of the vector store.
        @type vector_store_lfn: str
        @param vector_store_name: The name of the vector store.
        @type vector_store_name: str
        @param vector_store_protocol: The protocol of the vector store.
        @type vector_store_protocol: ProtocolEnum
        @param embedding_model_id: The ID of the embedding model used to create the vector store.
        @type embedding_model_id: int
        """
        pass
