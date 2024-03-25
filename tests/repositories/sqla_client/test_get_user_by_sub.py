from faker import Faker
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLAClient


def test_client_by_sub(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
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

        dto = client_repository.get_client_by_sub(client_sub=client_sub)

        assert dto.status == True
        assert dto.errorCode == None
        assert dto.data is not None
        assert dto.data.sub == client_sub


def test_error_get_client_by_sub_none_client_sub(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    client_repository = app_initialization_container.sqla_client_repository()

    dto = client_repository.get_client_by_sub(client_sub=None)  # type: ignore

    assert dto.status == False
    assert dto.errorCode == -1
    assert dto.errorName == "Client SUB not provided"
    assert dto.errorType == "ClientSubNotProvided"
