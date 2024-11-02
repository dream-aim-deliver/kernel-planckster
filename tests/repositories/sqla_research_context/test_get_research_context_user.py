import random
import uuid

from faker import Faker
from lib.core.dto.research_context_repository_dto import GetResearchContextClientDTO
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLALLM, SQLAResearchContext, SQLAClient


def test_get_research_context_client(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client: SQLAClient,
) -> None:
    sqla_research_context_repository = app_initialization_container.sqla_research_context_repository()

    fake_clients = []
    rand_int_1 = random.randint(1, 10)
    for _ in range(rand_int_1):
        fake_client = SQLAClient(sub=fake.name())
        fake_clients.append(fake_client)

    client = fake_client

    research_contexts = []
    rand_int_2 = random.randint(1, 10)
    for _ in range(rand_int_2):
        research_context = SQLAResearchContext(
            title=fake.name(), description=fake.text(), external_id=str(uuid.uuid4())
        )
        research_contexts.append(research_context)

    client.research_contexts = research_contexts
    client_sub = client.sub

    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=client.research_contexts,
    )

    research_context_titles = [research_context.title for research_context in client.research_contexts]

    research_context_title = random.choice(research_context_titles)

    with db_session() as session:
        for fake_client in fake_clients:
            fake_client.save(session=session, flush=True)
        llm.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        sqla_research_context = session.query(SQLAResearchContext).filter_by(title=research_context_title).first()

        assert sqla_research_context is not None

        get_client_DTO: GetResearchContextClientDTO = sqla_research_context_repository.get_research_context_client(
            research_context_id=sqla_research_context.id
        )

        assert get_client_DTO is not None
        assert get_client_DTO.status == True
        assert get_client_DTO.data is not None
        assert get_client_DTO.data.sub == client_sub


def test_error_get_research_context_client_id_is_None(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
) -> None:
    sqla_research_context_repository = app_initialization_container.sqla_research_context_repository()

    get_client_DTO: GetResearchContextClientDTO = sqla_research_context_repository.get_research_context_client(research_context_id=None)  # type: ignore

    assert get_client_DTO.status == False
    assert get_client_DTO.errorCode == -1
    assert get_client_DTO.errorMessage == "Research Context ID cannot be None"
    assert get_client_DTO.errorName == "Research Context ID not provided"
    assert get_client_DTO.errorType == "ResearchContextIdNotProvided"


def test_error_get_research_context_client_rc_not_found_by_id(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
) -> None:
    sqla_research_context_repository = app_initialization_container.sqla_research_context_repository()

    irrealistic_id = 99999999

    get_research_context_DTO: GetResearchContextClientDTO = (
        sqla_research_context_repository.get_research_context_client(research_context_id=irrealistic_id)
    )

    assert get_research_context_DTO.status == False
    assert get_research_context_DTO.errorCode == -1
    assert (
        get_research_context_DTO.errorMessage == f"Research Context with ID {irrealistic_id} not found in the database."
    )
    assert get_research_context_DTO.errorName == "Research Context not found"
    assert get_research_context_DTO.errorType == "ResearchContextNotFound"
