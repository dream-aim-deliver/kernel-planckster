import random
from faker import Faker
from lib.core.dto.research_context_repository_dto import GetResearchContextDTO
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLALLM, SQLAResearchContext, SQLAUser


def test_get_research_context(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_user: SQLAUser,
) -> None:
    sqla_research_context_repository = app_initialization_container.sqla_research_context_repository()

    user = fake_user

    research_contexts = []
    for _ in range(10):
        research_context = SQLAResearchContext(
            title=fake.name(),
        )
        research_contexts.append(research_context)

    user.research_contexts = research_contexts

    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=user.research_contexts,
    )

    research_context_titles = [research_context.title for research_context in user.research_contexts]

    rand_int = random.randint(0, len(research_context_titles) - 1)
    research_context_title = research_context_titles[rand_int]

    with db_session() as session:
        llm.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        sqla_research_context = session.query(SQLAResearchContext).filter_by(title=research_context_title).first()

        assert sqla_research_context is not None

        get_research_context_DTO: GetResearchContextDTO = sqla_research_context_repository.get_research_context(
            research_context_id=sqla_research_context.id
        )

        assert get_research_context_DTO is not None
        assert get_research_context_DTO.status == True
        assert get_research_context_DTO.data is not None
        assert get_research_context_DTO.data.title == research_context_title


def test_error_get_research_context_id_is_None(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
) -> None:
    sqla_research_context_repository = app_initialization_container.sqla_research_context_repository()

    get_research_context_DTO: GetResearchContextDTO = sqla_research_context_repository.get_research_context(research_context_id=None)  # type: ignore

    assert get_research_context_DTO.status == False
    assert get_research_context_DTO.errorCode == -1
    assert get_research_context_DTO.errorMessage == "Research Context ID cannot be None"
    assert get_research_context_DTO.errorName == "Research Context ID not provided"
    assert get_research_context_DTO.errorType == "ResearchContextIdNotProvided"


def test_error_get_research_context_not_found_by_id(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
) -> None:
    sqla_research_context_repository = app_initialization_container.sqla_research_context_repository()

    irrealistic_id = 99999999

    get_research_context_DTO: GetResearchContextDTO = sqla_research_context_repository.get_research_context(
        research_context_id=irrealistic_id
    )

    assert get_research_context_DTO.status == False
    assert get_research_context_DTO.errorCode == -1
    assert (
        get_research_context_DTO.errorMessage == f"Research Context with ID {irrealistic_id} not found in the database."
    )
    assert get_research_context_DTO.errorName == "Research Context not found"
    assert get_research_context_DTO.errorType == "ResearchContextNotFound"
