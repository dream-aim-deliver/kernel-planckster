from faker import Faker
from lib.core.dto.client_repository_dto import ListResearchContextsDTO
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLALLM, SQLAResearchContext, SQLAClient


def test_list_research_contexts_in_client(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client: SQLAClient,
) -> None:
    sqla_client_repository = app_initialization_container.sqla_client_repository()

    client = fake_client

    research_contexts = []
    for _ in range(10):
        research_context = SQLAResearchContext(
            title=fake.name(),
            description=fake.text(),
        )
        research_contexts.append(research_context)

    client.research_contexts = research_contexts
    client_sub = client.sub

    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=client.research_contexts,
    )

    research_context_titles = [research_context.title for research_context in client.research_contexts]

    with db_session() as session:
        llm.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        sqla_client = session.query(SQLAClient).filter_by(sub=client_sub).first()

        assert sqla_client is not None

        list_research_contexts_DTO: ListResearchContextsDTO = sqla_client_repository.list_research_contexts(
            client_id=sqla_client.id
        )

        assert list_research_contexts_DTO is not None
        assert list_research_contexts_DTO.status == True
        assert list_research_contexts_DTO.data is not None

        sqla_rc_titles = [research_context.title for research_context in list_research_contexts_DTO.data]

        for title in research_context_titles:
            assert title in sqla_rc_titles


def test_empty_list_research_contexts_in_client(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client: SQLAClient,
) -> None:
    sqla_client_repository = app_initialization_container.sqla_client_repository()

    client = fake_client
    client_sub = client.sub

    with db_session() as session:
        client.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        sqla_client = session.query(SQLAClient).filter_by(sub=client_sub).first()

        assert sqla_client is not None

        list_research_contexts_DTO: ListResearchContextsDTO = sqla_client_repository.list_research_contexts(
            client_id=sqla_client.id
        )

        assert list_research_contexts_DTO is not None
        assert list_research_contexts_DTO.status == True
        assert list_research_contexts_DTO.data == []


def test_error_list_research_contexts_client_id_is_none(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
) -> None:
    sqla_client_repository = app_initialization_container.sqla_client_repository()

    list_research_contexts_DTO: ListResearchContextsDTO = sqla_client_repository.list_research_contexts(client_id=None)

    assert list_research_contexts_DTO is not None
    assert list_research_contexts_DTO.status == False
    assert list_research_contexts_DTO.errorCode == -1
    assert list_research_contexts_DTO.errorMessage == "Client ID cannot be None"
    assert list_research_contexts_DTO.errorName == "Client ID not provided"
    assert list_research_contexts_DTO.errorType == "ClientIdNotProvided"


def test_error_list_research_contexts_client_not_found_by_id(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
) -> None:
    sqla_client_repository = app_initialization_container.sqla_client_repository()

    irrealistic_id = 99999999

    list_research_contexts_DTO: ListResearchContextsDTO = sqla_client_repository.list_research_contexts(
        client_id=irrealistic_id
    )

    assert list_research_contexts_DTO is not None
    assert list_research_contexts_DTO.status == False
    assert list_research_contexts_DTO.errorCode == -1
    assert list_research_contexts_DTO.errorMessage == f"Client with ID {irrealistic_id} not found in the database"
    assert list_research_contexts_DTO.errorName == "Client not found"
    assert list_research_contexts_DTO.errorType == "ClientNotFound"
