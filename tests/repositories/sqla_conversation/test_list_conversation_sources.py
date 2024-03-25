import random
from typing import List
import uuid
from faker import Faker
from lib.core.dto.conversation_repository_dto import (
    ListConversationSourcesDTO,
)
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory

from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLACitation,
    SQLAConversation,
    SQLAClient,
)


def test_list_conversation_sources(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client_with_conversation: SQLAClient,
    fake_client_with_source_data: SQLAClient,
    fake_citations: List[SQLACitation],
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    client_with_conv = fake_client_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=client_with_conv.research_contexts,
    )

    researchContext = random.choice(client_with_conv.research_contexts)

    sqla_client_with_sd = fake_client_with_source_data
    source_data = sqla_client_with_sd.source_data

    researchContext.source_data = source_data

    conversation = random.choice(researchContext.conversations)
    conversation.title = f"{conversation.title}-{uuid.uuid4()}"
    conversation_title = conversation.title

    citations = fake_citations

    source_data_names_used: List[str] = []
    source_data_rel_paths_used: List[str] = []

    for message in conversation.messages:
        if message.type == "agent_message":
            citation = random.choice(citations)
            random_source_datum = random.choice(source_data)
            random_source_datum.citations.append(citation)
            message.citations.append(citation)
            citations.remove(citation)

    with db_session() as session:
        researchContext.save(session=session, flush=True)
        session.commit()

        conv = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        assert conv is not None

        conv_id = conv.id

        dto: ListConversationSourcesDTO = conversation_repository.list_conversation_sources(conversation_id=conv_id)

        assert dto.data is not None

        sql_srcs_names = tuple(source.name for source in dto.data)
        sql_srcs_rel_paths = tuple(source.relative_path for source in dto.data)

        assert dto.status == True
        assert dto.errorCode == None
        assert isinstance(dto.data, list)

        for name in source_data_names_used:
            assert name in sql_srcs_names

        for rel_path in source_data_rel_paths_used:
            assert rel_path in sql_srcs_rel_paths


def test_error_list_conversation_sources_none_conversation_id(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    dto: ListConversationSourcesDTO = conversation_repository.list_conversation_sources(conversation_id=None)  # type: ignore

    assert dto.status == False
    assert dto.errorCode == -1
    assert dto.errorMessage == "Conversation ID cannot be None"
    assert dto.errorName == "Conversation ID not provided"
    assert dto.errorType == "ConversationIdNotProvided"


def test_error_list_conversation_sources_none_sqla_conversation(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    irrealistic_ID = 99999999
    dto: ListConversationSourcesDTO = conversation_repository.list_conversation_sources(conversation_id=irrealistic_ID)

    assert dto.status == False
    assert dto.errorCode == -1
    assert dto.errorMessage == f"Conversation with ID {irrealistic_ID} not found in the database."
    assert dto.errorName == "Conversation not found"
    assert dto.errorType == "ConversationNotFound"


def test_error_list_conversation_sources_research_context_no_source_data(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client_with_conversation: SQLAClient,
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    client_with_conv = fake_client_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=client_with_conv.research_contexts,
    )
    researchContext = client_with_conv.research_contexts[0]

    conversation = researchContext.conversations[0]
    conversation.title = f"{conversation.title}-{uuid.uuid4()}"
    conversation_title = conversation.title

    with db_session() as session:
        researchContext.save(session=session, flush=True)
        session.commit()

    conv_id = None
    with db_session() as session:
        conv_sqla_query = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        if conv_sqla_query is None:
            raise Exception("Conversation not found")

        conv_id = conv_sqla_query.id
        messages = conv_sqla_query.messages
        agent_messages = [message for message in messages if message.type == "agent_message"]
        agent_messages_ids = [message.id for message in agent_messages]

        dto: ListConversationSourcesDTO = conversation_repository.list_conversation_sources(conversation_id=conv_id)

    assert dto.status == False
    assert dto.errorCode == -1
    assert dto.errorMessage == f"Message Responses with ID {agent_messages_ids} have no source data."
    assert dto.errorName == "Message Responses have no source data"
    assert dto.errorType == "AgentMessagesHaveNoSourceData"
