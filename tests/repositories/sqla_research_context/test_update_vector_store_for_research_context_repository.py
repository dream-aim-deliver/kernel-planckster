import random
from typing import List
from lib.core.dto.research_context_repository_dto import UpdateResearchContextVectorStoreDTO
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


def test_update_vector_store_research_context(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_user_with_conversation: SQLAUser,
    fake_llm: SQLALLM,
    fake_embedding_model_with_vector_stores: SQLAEmbeddingModel,
) -> None:
    sqla_research_context_repository = app_initialization_container.sqla_research_context_repository()

    user_with_conv = fake_user_with_conversation
    llm = fake_llm
    llm.research_contexts = user_with_conv.research_contexts

    embedding_model_with_vector_store = fake_embedding_model_with_vector_stores

    with db_session() as session:
        session.add(user_with_conv)
        session.add(embedding_model_with_vector_store)
        session.commit()
        rand_int_1 = random.randint(0, len(user_with_conv.research_contexts) - 1)
        research_context = user_with_conv.research_contexts[rand_int_1]
        research_context_id = research_context.id
        rand_int_2 = random.randint(0, len(embedding_model_with_vector_store.vector_stores) - 1)
        vector_store = embedding_model_with_vector_store.vector_stores[rand_int_2]
        vector_store_lfn = vector_store.lfn
        vector_store_id = vector_store.id

    with db_session() as session:
        update_rc_vs_dto: UpdateResearchContextVectorStoreDTO = (
            sqla_research_context_repository.update_research_context_vector_store(
                research_context_id=research_context_id,
                vector_store_id=vector_store_id,
            )
        )

        assert update_rc_vs_dto.status == True
        assert update_rc_vs_dto.vector_store_id is not None

    with db_session() as session:
        queried_research_context = session.get(SQLAResearchContext, research_context_id)

        assert queried_research_context is not None
        assert queried_research_context.vector_store.id == vector_store_id
        assert queried_research_context.vector_store.lfn == vector_store_lfn


def test_error_update_research_context_id_is_none(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_embedding_model_with_vector_stores: SQLAEmbeddingModel,
) -> None:
    sqla_research_context_repository = app_initialization_container.sqla_research_context_repository()

    embedding_model_with_vector_stores = fake_embedding_model_with_vector_stores

    with db_session() as session:
        session.add(embedding_model_with_vector_stores)
        session.commit()
        rand_int_1 = random.randint(0, len(embedding_model_with_vector_stores.vector_stores) - 1)
        vector_store = embedding_model_with_vector_stores.vector_stores[rand_int_1]
        vector_store_id = vector_store.id

    with db_session() as session:
        update_rc_vs_dto: UpdateResearchContextVectorStoreDTO = (
            sqla_research_context_repository.update_research_context_vector_store(
                research_context_id=None,  # type: ignore
                vector_store_id=vector_store_id,
            )
        )

        assert update_rc_vs_dto.status == False
        assert update_rc_vs_dto.errorCode == -1
        assert update_rc_vs_dto.errorMessage == "Research Context ID cannot be None"
        assert update_rc_vs_dto.errorName == "Research Context ID not provided"
        assert update_rc_vs_dto.errorType == "ResearchContextIdNotProvided"


def test_error_update_research_context_vector_store_id_is_None(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_user_with_conversation: SQLAUser,
    fake_llm: SQLALLM,
) -> None:
    sqla_research_context_repository = app_initialization_container.sqla_research_context_repository()

    user_with_conv = fake_user_with_conversation
    llm = fake_llm
    llm.research_contexts = user_with_conv.research_contexts

    with db_session() as session:
        session.add(user_with_conv)
        session.commit()
        rand_int_1 = random.randint(0, len(user_with_conv.research_contexts) - 1)
        research_context = user_with_conv.research_contexts[rand_int_1]
        research_context_id = research_context.id

    with db_session() as session:
        update_rc_vs_dto: UpdateResearchContextVectorStoreDTO = (
            sqla_research_context_repository.update_research_context_vector_store(
                research_context_id=research_context_id,
                vector_store_id=None,  # type: ignore
            )
        )

    assert update_rc_vs_dto.status == False
    assert update_rc_vs_dto.errorCode == -1
    assert update_rc_vs_dto.errorMessage == "Vector Store ID cannot be None"
    assert update_rc_vs_dto.errorName == "Vector Store ID not provided"
    assert update_rc_vs_dto.errorType == "VectorStoreIdNotProvided"


def test_error_update_research_context_vector_store_sqla_research_context_not_found(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_embedding_model_with_vector_stores: SQLAEmbeddingModel,
) -> None:
    sqla_research_context_repository = app_initialization_container.sqla_research_context_repository()

    embedding_model = fake_embedding_model_with_vector_stores

    with db_session() as session:
        session.add(embedding_model)
        session.commit()
        rand_int_1 = random.randint(0, len(embedding_model.vector_stores) - 1)
        vector_store = embedding_model.vector_stores[rand_int_1]
        vector_store_id = vector_store.id

    with db_session() as session:
        irrealistic_ID = 99999999
        update_rc_vs_dto: UpdateResearchContextVectorStoreDTO = (
            sqla_research_context_repository.update_research_context_vector_store(
                research_context_id=irrealistic_ID,
                vector_store_id=vector_store_id,
            )
        )

        assert update_rc_vs_dto.status == False
        assert update_rc_vs_dto.errorCode == -1
        assert update_rc_vs_dto.errorMessage == f"Research Context with ID {irrealistic_ID} not found in the database."
        assert update_rc_vs_dto.errorName == "Research Context not found"
        assert update_rc_vs_dto.errorType == "ResearchContextNotFound"


def test_error_update_research_context_vector_store_sqla_vector_store_not_found(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_user_with_conversation: SQLAUser,
    fake_llm: SQLALLM,
) -> None:
    sqla_research_context_repository = app_initialization_container.sqla_research_context_repository()

    user_with_conv = fake_user_with_conversation
    llm = fake_llm
    llm.research_contexts = user_with_conv.research_contexts

    with db_session() as session:
        session.add(user_with_conv)
        session.commit()
        research_context = user_with_conv.research_contexts[0]
        research_context_id = research_context.id

    with db_session() as session:
        irrealistic_ID = 99999999
        update_rc_vs_dto: UpdateResearchContextVectorStoreDTO = (
            sqla_research_context_repository.update_research_context_vector_store(
                research_context_id=research_context_id,
                vector_store_id=irrealistic_ID,
            )
        )

        assert update_rc_vs_dto.status == False
        assert update_rc_vs_dto.errorCode == -1
        assert update_rc_vs_dto.errorMessage == f"Vector Store with ID {irrealistic_ID} not found in the database."
        assert update_rc_vs_dto.errorName == "Vector Store not found"
        assert update_rc_vs_dto.errorType == "VectorStoreNotFound"
