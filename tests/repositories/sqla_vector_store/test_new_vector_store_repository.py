import random
from typing import List
from lib.core.dto.research_context_repository_dto import UpdateResearchContextVectorStoreDTO
from lib.core.dto.vector_store_dto import NewVectorStoreDTO
from lib.core.entity.models import ProtocolEnum
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAEmbeddingModel,
    SQLAResearchContext,
    SQLAUser,
    SQLAVectorStore,
)


def test_new_vector_store(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_embedding_model_with_vector_stores: SQLAEmbeddingModel,
    fake_lfn_list: List[str],
) -> None:
    sqla_vector_store_repository = app_initialization_container.sqla_vector_store_repository()

    embedding_model_with_vector_stores = fake_embedding_model_with_vector_stores

    rand_int_1 = random.randint(0, len(fake_lfn_list) - 1)
    new_vector_store_lfn = fake_lfn_list[rand_int_1]
    new_vector_store_name = new_vector_store_lfn.split("/")[-1]
    new_vector_store_protocol_str = new_vector_store_lfn.split("://")[0]
    new_vector_store_protocol = ProtocolEnum(new_vector_store_protocol_str)

    with db_session() as session:
        session.add(embedding_model_with_vector_stores)
        session.commit()
        embedding_model_id = embedding_model_with_vector_stores.id

    with db_session() as session:
        new_vs_dto: NewVectorStoreDTO = sqla_vector_store_repository.new_vector_store(
            embedding_model_id=embedding_model_id,
            vector_store_name=new_vector_store_name,
            vector_store_lfn=new_vector_store_lfn,
            vector_store_protocol=new_vector_store_protocol,
        )

        assert new_vs_dto.status == True
        assert new_vs_dto.vector_store_id is not None

    with db_session() as session:
        queried_new_vector_store = session.get(SQLAVectorStore, new_vs_dto.vector_store_id)

        assert queried_new_vector_store is not None
        assert queried_new_vector_store.name == new_vector_store_name
        assert queried_new_vector_store.lfn == new_vector_store_lfn
        assert queried_new_vector_store.protocol == new_vector_store_protocol
        assert queried_new_vector_store.embedding_model_id == embedding_model_id


def test_error_new_vector_store_vector_store_lfn_is_none(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    sqla_vector_store_repository = app_initialization_container.sqla_vector_store_repository()

    new_vs_dto: NewVectorStoreDTO = sqla_vector_store_repository.new_vector_store(
        embedding_model_id=1,
        vector_store_name="test",
        vector_store_lfn=None,  # type: ignore
        vector_store_protocol=ProtocolEnum.S3,
    )

    assert new_vs_dto.status == False
    assert new_vs_dto.errorCode == -1
    assert new_vs_dto.errorMessage == "Vector Store LFN cannot be None"
    assert new_vs_dto.errorName == "Vector Store LFN not provided"
    assert new_vs_dto.errorType == "VectorStoreLFNNotProvided"


def test_error_new_vector_store_vector_store_name_is_none(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    sqla_vector_store_repository = app_initialization_container.sqla_vector_store_repository()

    new_vs_dto: NewVectorStoreDTO = sqla_vector_store_repository.new_vector_store(
        embedding_model_id=1,
        vector_store_name=None,  # type: ignore
        vector_store_lfn="test",
        vector_store_protocol=ProtocolEnum.S3,
    )

    assert new_vs_dto.status == False
    assert new_vs_dto.errorCode == -1
    assert new_vs_dto.errorMessage == "Vector Store name cannot be None"
    assert new_vs_dto.errorName == "Vector Store name not provided"
    assert new_vs_dto.errorType == "VectorStoreNameNotProvided"


def test_error_new_vector_store_vector_store_protocol_is_none(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    sqla_vector_store_repository = app_initialization_container.sqla_vector_store_repository()

    new_vs_dto: NewVectorStoreDTO = sqla_vector_store_repository.new_vector_store(
        embedding_model_id=1,
        vector_store_name="test",
        vector_store_lfn="test",
        vector_store_protocol=None,  # type: ignore
    )

    assert new_vs_dto.status == False
    assert new_vs_dto.errorCode == -1
    assert new_vs_dto.errorMessage == "Vector Store protocol cannot be None"
    assert new_vs_dto.errorName == "Vector Store protocol not provided"
    assert new_vs_dto.errorType == "VectorStoreProtocolNotProvided"


def test_error_new_vector_store_embedding_model_id_is_none(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    sqla_vector_store_repository = app_initialization_container.sqla_vector_store_repository()

    new_vs_dto: NewVectorStoreDTO = sqla_vector_store_repository.new_vector_store(
        embedding_model_id=None,  # type: ignore
        vector_store_name="test",
        vector_store_lfn="test",
        vector_store_protocol=ProtocolEnum.S3,
    )

    assert new_vs_dto.status == False
    assert new_vs_dto.errorCode == -1
    assert new_vs_dto.errorMessage == "Embedding Model ID cannot be None"
    assert new_vs_dto.errorName == "Embedding Model ID not provided"
    assert new_vs_dto.errorType == "EmbeddingModelIdNotProvided"


def test_error_new_vector_store_sqla_embedding_model_not_found(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_user_with_conversation: SQLAUser,
    fake_llm: SQLALLM,
) -> None:
    sqla_vector_store_repository = app_initialization_container.sqla_vector_store_repository()

    irrealistic_ID = 99999999
    new_vs_dto: NewVectorStoreDTO = sqla_vector_store_repository.new_vector_store(
        embedding_model_id=irrealistic_ID,
        vector_store_name="test",
        vector_store_lfn="test",
        vector_store_protocol=ProtocolEnum.S3,
    )

    assert new_vs_dto.status == False
    assert new_vs_dto.errorCode == -1
    assert new_vs_dto.errorMessage == f"Embedding Model with ID {irrealistic_ID} not found in the database."
    assert new_vs_dto.errorName == "Embedding Model not found"
    assert new_vs_dto.errorType == "EmbeddingModelNotFound"
