from faker import Faker
from lib.core.dto.user_repository_dto import ListUserResearchContextsDTO
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLALLM, SQLAResearchContext, SQLAUser


def test_list_research_contexts_in_user(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_user: SQLAUser,
) -> None:
    sqla_user_repository = app_initialization_container.sqla_user_repository()

    user = fake_user

    research_contexts = []
    for _ in range(10):
        research_context = SQLAResearchContext(
            title=fake.name(),
        )
        research_contexts.append(research_context)

    user.research_contexts = research_contexts
    user_sid = user.sid

    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=user.research_contexts,
    )

    research_context_titles = [research_context.title for research_context in user.research_contexts]

    with db_session() as session:
        llm.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        sqla_user = session.query(SQLAUser).filter_by(sid=user_sid).first()

        assert sqla_user is not None

        list_research_contexts_DTO: ListUserResearchContextsDTO = sqla_user_repository.list_research_contexts(
            user_id=sqla_user.id
        )

        assert list_research_contexts_DTO is not None
        assert list_research_contexts_DTO.status == True
        assert list_research_contexts_DTO.data is not None

        sqla_rc_titles = [research_context.title for research_context in list_research_contexts_DTO.data]

        for title in research_context_titles:
            assert title in sqla_rc_titles


def test_empty_list_research_contexts_in_user(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_user: SQLAUser,
) -> None:
    sqla_user_repository = app_initialization_container.sqla_user_repository()

    user = fake_user
    user_sid = user.sid

    with db_session() as session:
        user.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        sqla_user = session.query(SQLAUser).filter_by(sid=user_sid).first()

        assert sqla_user is not None

        list_research_contexts_DTO: ListUserResearchContextsDTO = sqla_user_repository.list_research_contexts(
            user_id=sqla_user.id
        )

        assert list_research_contexts_DTO is not None
        assert list_research_contexts_DTO.status == True
        assert list_research_contexts_DTO.data == []


def test_error_list_research_contexts_user_id_is_none(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
) -> None:
    sqla_user_repository = app_initialization_container.sqla_user_repository()

    list_research_contexts_DTO: ListUserResearchContextsDTO = sqla_user_repository.list_research_contexts(user_id=None)  # type: ignore

    assert list_research_contexts_DTO is not None
    assert list_research_contexts_DTO.status == False
    assert list_research_contexts_DTO.errorCode == -1
    assert list_research_contexts_DTO.errorMessage == "User ID cannot be None"
    assert list_research_contexts_DTO.errorName == "User ID not provided"
    assert list_research_contexts_DTO.errorType == "UserIdNotProvided"


def test_error_list_research_contexts_user_not_found_by_id(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
) -> None:
    sqla_user_repository = app_initialization_container.sqla_user_repository()

    irrealistic_id = 99999999

    list_research_contexts_DTO: ListUserResearchContextsDTO = sqla_user_repository.list_research_contexts(
        user_id=irrealistic_id
    )

    assert list_research_contexts_DTO is not None
    assert list_research_contexts_DTO.status == False
    assert list_research_contexts_DTO.errorCode == -1
    assert list_research_contexts_DTO.errorMessage == f"User with ID {irrealistic_id} not found in the database"
    assert list_research_contexts_DTO.errorName == "User not found"
    assert list_research_contexts_DTO.errorType == "UserNotFound"
