import random
from faker import Faker
from lib.core.dto.research_context_repository_dto import ListResearchContextConversationsDTO
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLALLM, SQLAResearchContext, SQLAClient


def test_list_conversations_in_research_context(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client_with_conversation: SQLAClient,
) -> None:
    sqla_research_context_repository = app_initialization_container.sqla_research_context_repository()

    client_with_conv = fake_client_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=client_with_conv.research_contexts,
    )

    research_context = random.choice(client_with_conv.research_contexts)
    research_context_title = research_context.title

    conversations = research_context.conversations
    conversation_titles = [conversation.title for conversation in conversations]

    with db_session() as session:
        client_with_conv.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        sqla_research_context = session.query(SQLAResearchContext).filter_by(title=research_context_title).first()

        assert sqla_research_context is not None

        list_convs_DTO: ListResearchContextConversationsDTO = sqla_research_context_repository.list_conversations(
            sqla_research_context.id
        )
        assert list_convs_DTO is not None
        assert list_convs_DTO.status == True
        assert list_convs_DTO.data is not None

        sql_convs_titles = [conversation.title for conversation in list_convs_DTO.data]

        for title in conversation_titles:
            assert title in sql_convs_titles


def test_empty_list_conversations_in_research_context(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client: SQLAClient,
) -> None:
    sqla_research_context_repository = app_initialization_container.sqla_research_context_repository()

    research_context = SQLAResearchContext(
        title=fake.name(),
        description=fake.text(),
    )

    client = fake_client
    client.research_contexts.append(research_context)

    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=client.research_contexts,
    )

    research_context_title = client.research_contexts[0].title

    with db_session() as session:
        client.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        sqla_research_context = session.query(SQLAResearchContext).filter_by(title=research_context_title).first()

        assert sqla_research_context is not None

        list_convs_DTO: ListResearchContextConversationsDTO = sqla_research_context_repository.list_conversations(
            sqla_research_context.id
        )
        assert list_convs_DTO is not None
        assert list_convs_DTO.status == True
        assert list_convs_DTO.data == []


def test_error_list_conversations_research_context_id_is_None(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
) -> None:
    sqla_research_context_repository = app_initialization_container.sqla_research_context_repository()

    list_convs_DTO: ListResearchContextConversationsDTO = sqla_research_context_repository.list_conversations(
        research_context_id=None
    )

    assert list_convs_DTO is not None
    assert list_convs_DTO.status == False
    assert list_convs_DTO.errorCode == -1
    assert list_convs_DTO.errorMessage == "Research Context ID cannot be None"
    assert list_convs_DTO.errorName == "Research Context ID not provided"
    assert list_convs_DTO.errorType == "ResearchContextIdNotProvided"


def test_error_list_conversations_research_context_not_found_by_id(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
) -> None:
    sqla_research_context_repository = app_initialization_container.sqla_research_context_repository()

    irrealistic_id = 99999999

    list_convs_DTO: ListResearchContextConversationsDTO = sqla_research_context_repository.list_conversations(
        research_context_id=irrealistic_id
    )

    assert list_convs_DTO is not None
    assert list_convs_DTO.status == False
    assert list_convs_DTO.errorCode == -1
    assert list_convs_DTO.errorMessage == f"Research Context with ID {irrealistic_id} not found in the database"
    assert list_convs_DTO.errorName == "Research Context not found"
    assert list_convs_DTO.errorType == "ResearchContextNotFound"
