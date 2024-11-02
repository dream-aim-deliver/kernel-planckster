import random
import uuid

from faker import Faker
from lib.core.dto.research_context_repository_dto import ListSourceDataDTO
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLALLM, SQLAResearchContext, SQLAClient
from lib.infrastructure.repository.sqla.utils import convert_sqla_source_data_to_core_source_data


def test_list_source_data_of_research_context(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client_with_conversation: SQLAClient,
    fake_client_with_source_data: SQLAClient,
) -> None:
    research_context_repository = app_initialization_container.sqla_research_context_repository()

    client_with_conv = fake_client_with_conversation
    client_with_sd = fake_client_with_source_data

    research_context = random.choice(client_with_conv.research_contexts)

    for source_datum in client_with_sd.source_data:
        research_context.source_data.append(source_datum)

    source_data = research_context.source_data

    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=client_with_conv.research_contexts,
    )

    with db_session() as session:
        session.add(research_context)
        session.commit()

        dto: ListSourceDataDTO = research_context_repository.list_source_data(research_context.id)

        assert dto.status == True
        assert dto.errorCode == None

        assert dto.data is not None

        core_sd_list = [convert_sqla_source_data_to_core_source_data(sd) for sd in source_data]

        assert dto.data == core_sd_list


def test_empty_list_source_data_of_research_context(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client: SQLAClient,
) -> None:
    research_context_repository = app_initialization_container.sqla_research_context_repository()

    research_context = SQLAResearchContext(
        title=fake.name(),
        description=fake.text(),
        external_id=str(uuid.uuid4()),
        client=fake_client,
    )

    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=[research_context],
    )

    with db_session() as session:
        session.add(research_context)
        session.commit()

        dto: ListSourceDataDTO = research_context_repository.list_source_data(research_context.id)

        assert dto.status == True
        assert dto.data == []
        assert dto.errorCode == None
        assert dto.errorMessage == None


def test_error_list_source_data_research_context_id_is_None(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    research_context_repository = app_initialization_container.sqla_research_context_repository()

    dto: ListSourceDataDTO = research_context_repository.list_source_data(research_context_id=None)  # type: ignore

    assert dto.status == False
    assert dto.errorCode == -1
    assert dto.errorMessage == "Research Context ID cannot be None"
    assert dto.errorName == "Research Context ID not provided"
    assert dto.errorType == "ResearchContextIdNotProvided"
    assert dto.data == None


def test_error_list_source_data_research_context_not_found_by_id(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
) -> None:
    research_context_repository = app_initialization_container.sqla_research_context_repository()

    irrealistic_id = 999999999
    dto: ListSourceDataDTO = research_context_repository.list_source_data(research_context_id=irrealistic_id)

    assert dto.status == False
    assert dto.errorCode == -1
    assert dto.errorMessage == f"Research context with ID {irrealistic_id} not found in the database."
    assert dto.errorName == "Research Context not found"
    assert dto.errorType == "ResearchContextNotFound"
    assert dto.data == None
