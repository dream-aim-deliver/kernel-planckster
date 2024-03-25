from faker import Faker
from lib.core.dto.client_repository_dto import GetClientDTO
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLAClient


def test_get_client(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client: SQLAClient,
) -> None:
    client_repository = app_initialization_container.sqla_client_repository()

    client = fake_client
    client_sub = client.sub

    with db_session() as session:
        client.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        result = session.query(SQLAClient).filter_by(sub=client_sub).first()

        assert result is not None

        get_client_DTO = client_repository.get_client(client_id=result.id)

    assert get_client_DTO.status == True
    assert get_client_DTO.errorCode == None
    assert get_client_DTO.data is not None
    assert get_client_DTO.data.sub == client_sub


def test_error_get_client_none_client_id(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    client_repository = app_initialization_container.sqla_client_repository()

    get_client_DTO: GetClientDTO = client_repository.get_client(client_id=None)  # type: ignore

    assert get_client_DTO.status == False
    assert get_client_DTO.errorCode == -1
    assert get_client_DTO.errorMessage == "Client ID cannot be None"
    assert get_client_DTO.errorName == "Client ID not provided"
    assert get_client_DTO.errorType == "ClientIdNotProvided"


def test_error_get_client_none_sqla_client(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    client_repository = app_initialization_container.sqla_client_repository()

    irrealistic_ID = 99999999
    get_client_DTO: GetClientDTO = client_repository.get_client(client_id=irrealistic_ID)

    assert get_client_DTO.status == False
    assert get_client_DTO.errorCode == -1
    assert get_client_DTO.errorMessage == f"Client with ID {irrealistic_ID} not found in the database"
    assert get_client_DTO.errorName == "Client not found"
    assert get_client_DTO.errorType == "ClientNotFound"
