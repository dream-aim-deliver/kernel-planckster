import random
from typing import List
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
    SQLAKnowledgeSource,
    SQLAUser,
)


def test_list_conversation_sources(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_user_with_conversation: SQLAUser,
    fake_knowledge_source_with_source_data: SQLAKnowledgeSource,
    fake_citations: List[SQLACitation],
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    user_with_conv = fake_user_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=user_with_conv.research_contexts,
    )

    rand_int_1 = random.randint(0, len(user_with_conv.research_contexts) - 1)
    researchContext = user_with_conv.research_contexts[rand_int_1]

    ks_with_sd = fake_knowledge_source_with_source_data
    source_data = ks_with_sd.source_data

    researchContext.source_data = source_data

    rand_int_2 = random.randint(0, len(researchContext.conversations) - 1)
    conversation = researchContext.conversations[rand_int_2]
    conversation_title = conversation.title

    citations = fake_citations

    source_data_names_used = []
    source_data_lfns_used = []
    for message in conversation.messages:
        if message.type == "message_response":
            citation = random.choice(citations)
            random_source_datum = random.choice(source_data)
            random_source_datum.citations.append(citation)
            source_data_names_used.append(random_source_datum.name)
            source_data_lfns_used.append(random_source_datum.lfn)
            message.citations.append(citation)
            citations.remove(citation)

    with db_session() as session:
        researchContext.save(session=session, flush=True)
        session.commit()

    id = None
    with db_session() as session:
        result = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        assert result is not None

        id = result.id

        list_conv_srcs_DTO: ListConversationSourcesDTO = conversation_repository.list_conversation_sources(
            conversation_id=id
        )

    assert list_conv_srcs_DTO.data is not None

    sql_srcs_names = tuple(source.name for source in list_conv_srcs_DTO.data)
    sql_srcs_lfns = tuple(source.lfn for source in list_conv_srcs_DTO.data)

    assert list_conv_srcs_DTO.status == True
    assert list_conv_srcs_DTO.errorCode == None
    assert isinstance(list_conv_srcs_DTO.data, list)

    for name in source_data_names_used:
        assert name in sql_srcs_names

    for lfn in source_data_lfns_used:
        assert lfn in sql_srcs_lfns


def test_error_list_conversation_sources_none_conversation_id(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    list_conv_srcs_DTO: ListConversationSourcesDTO = conversation_repository.list_conversation_sources(conversation_id=None)  # type: ignore

    assert list_conv_srcs_DTO.status == False
    assert list_conv_srcs_DTO.errorCode == -1
    assert list_conv_srcs_DTO.errorMessage == "Conversation ID cannot be None"
    assert list_conv_srcs_DTO.errorName == "Conversation ID not provided"
    assert list_conv_srcs_DTO.errorType == "ConversationIdNotProvided"


def test_error_list_conversation_sources_none_sqla_conversation(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    irrealistic_ID = 99999999
    list_conv_srcs_DTO: ListConversationSourcesDTO = conversation_repository.list_conversation_sources(
        conversation_id=irrealistic_ID
    )

    assert list_conv_srcs_DTO.status == False
    assert list_conv_srcs_DTO.errorCode == -1
    assert list_conv_srcs_DTO.errorMessage == f"Conversation with ID {irrealistic_ID} not found in the database."
    assert list_conv_srcs_DTO.errorName == "Conversation not found"
    assert list_conv_srcs_DTO.errorType == "ConversationNotFound"


def test_error_list_conversation_sources_research_context_no_source_data(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_user_with_conversation: SQLAUser,
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    user_with_conv = fake_user_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=user_with_conv.research_contexts,
    )
    researchContext = user_with_conv.research_contexts[0]

    conversation = researchContext.conversations[0]
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
        message_responses = [message for message in messages if message.type == "message_response"]
        message_responses_ids = [message.id for message in message_responses]

        list_conv_srcs_DTO: ListConversationSourcesDTO = conversation_repository.list_conversation_sources(
            conversation_id=conv_id
        )

    assert list_conv_srcs_DTO.status == False
    assert list_conv_srcs_DTO.errorCode == -1
    assert list_conv_srcs_DTO.errorMessage == f"Message Responses with ID {message_responses_ids} have no source data."
    assert list_conv_srcs_DTO.errorName == "Message Responses have no source data"
    assert list_conv_srcs_DTO.errorType == "MessageResponsesHaveNoSourceData"
