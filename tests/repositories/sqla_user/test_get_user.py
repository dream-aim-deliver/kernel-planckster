from faker import Faker
from lib.core.dto.user_repository_dto import GetUserDTO
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLAUser


def test_get_user(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_user: SQLAUser,
) -> None:
    user_repository = app_initialization_container.sqla_user_repository()

    user = fake_user
    user_sid = user.sid

    with db_session() as session:
        user.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        result = session.query(SQLAUser).filter_by(sid=user_sid).first()

        assert result is not None

        get_user_DTO = user_repository.get_user(user_id=result.id)

    assert get_user_DTO.status == True
    assert get_user_DTO.errorCode == None
    assert get_user_DTO.data is not None
    assert get_user_DTO.data.sid == user_sid


def test_error_get_user_none_user_id(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    user_repository = app_initialization_container.sqla_user_repository()

    get_user_DTO: GetUserDTO = user_repository.get_user(user_id=None)  # type: ignore

    assert get_user_DTO.status == False
    assert get_user_DTO.errorCode == -1
    assert get_user_DTO.errorMessage == "User ID cannot be None"
    assert get_user_DTO.errorName == "User ID not provided"
    assert get_user_DTO.errorType == "UserIdNotProvided"


def test_error_get_user_none_sqla_user(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    user_repository = app_initialization_container.sqla_user_repository()

    irrealistic_ID = 99999999
    get_user_DTO: GetUserDTO = user_repository.get_user(user_id=irrealistic_ID)

    assert get_user_DTO.status == False
    assert get_user_DTO.errorCode == -1
    assert get_user_DTO.errorMessage == f"User with ID {irrealistic_ID} not found in the database"
    assert get_user_DTO.errorName == "User not found"
    assert get_user_DTO.errorType == "UserNotFound"
