from sqlalchemy.orm.session import Session
from lib.core.dto.research_context_repository_dto import UpdateResearchContextVectorStoreDTO
from lib.core.dto.vector_store_dto import NewVectorStoreDTO
from lib.core.entity.models import ProtocolEnum

from lib.core.ports.secondary.vector_store_repository import VectorStoreRepositoryOutputPort
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLAEmbeddingModel, SQLAVectorStore


class SQLAVectorStoreRepository(VectorStoreRepositoryOutputPort):
    def __init__(self, session_factory: TDatabaseFactory) -> None:
        super().__init__()
        with session_factory() as session:
            self._session = session

    @property
    def session(self) -> Session:
        return self._session

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

        if vector_store_lfn is None:
            self.logger.error(f"Vector store LFN cannot be None")
            errorDTO = NewVectorStoreDTO(
                status=False,
                errorCode=-1,
                errorMessage="Vector Store LFN cannot be None",
                errorName="Vector Store LFN not provided",
                errorType="VectorStoreLFNNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if vector_store_name is None:
            self.logger.error(f"Vector store name cannot be None")
            errorDTO = NewVectorStoreDTO(
                status=False,
                errorCode=-1,
                errorMessage="Vector Store name cannot be None",
                errorName="Vector Store name not provided",
                errorType="VectorStoreNameNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if vector_store_protocol is None:
            self.logger.error(f"Vector store protocol cannot be None")
            errorDTO = NewVectorStoreDTO(
                status=False,
                errorCode=-1,
                errorMessage="Vector Store protocol cannot be None",
                errorName="Vector Store protocol not provided",
                errorType="VectorStoreProtocolNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if embedding_model_id is None:
            self.logger.error(f"Embedding model ID cannot be None")
            errorDTO = NewVectorStoreDTO(
                status=False,
                errorCode=-1,
                errorMessage="Embedding Model ID cannot be None",
                errorName="Embedding Model ID not provided",
                errorType="EmbeddingModelIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        queried_sqla_embedding_model: SQLAEmbeddingModel | None = self.session.get(
            SQLAEmbeddingModel, embedding_model_id
        )

        if queried_sqla_embedding_model is None:
            self.logger.error(f"Embedding model with ID {embedding_model_id} not found.")
            errorDTO = NewVectorStoreDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Embedding Model with ID {embedding_model_id} not found in the database.",
                errorName="Embedding Model not found",
                errorType="EmbeddingModelNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_new_vector_store: SQLAVectorStore = SQLAVectorStore(
            name=vector_store_name,
            lfn=vector_store_lfn,
            protocol=vector_store_protocol,
            embedding_model_id=embedding_model_id,
        )

        try:
            sqla_new_vector_store.save(session=self.session)
            self.session.commit()

            return NewVectorStoreDTO(status=True, vector_store_id=sqla_new_vector_store.id)

        except Exception as e:
            self.logger.error(f"Error while creating new vector store: {e}")
            errorDTO = NewVectorStoreDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error while creating new vector store: {e}",
                errorName="Error while creating new vector store",
                errorType="ErrorWhileCreatingNewVectorStore",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO
