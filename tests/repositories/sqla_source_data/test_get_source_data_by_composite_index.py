import random
from typing import List
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLAClient, SQLASourceData
from lib.infrastructure.repository.sqla.utils import (
    convert_sqla_source_data_to_core_source_data,
)


def test_get_source_data_by_composite_index(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_client_with_source_data_list: List[SQLAClient],
) -> None:
    sqla_source_data_repository = app_initialization_container.sqla_source_data_repository()

    sqla_clients = fake_client_with_source_data_list

    sqla_source_data_list: List[SQLASourceData] = []
    for client in sqla_clients:
        sqla_source_data_list.extend(client.source_data)

    sqla_source_data = random.choice(sqla_source_data_list)
    protocol = sqla_source_data.protocol
    relative_path = sqla_source_data.relative_path

    with db_session() as session:
        for client in sqla_clients:
            client.save(session=session, flush=True)
        session.commit()

        core_source_data = convert_sqla_source_data_to_core_source_data(sqla_source_data)

        dto = sqla_source_data_repository.get_source_data_by_composite_index(
            client_id=sqla_source_data.client.id, protocol=protocol, relative_path=relative_path
        )

        assert dto is not None
        assert dto.status == True
        assert dto.data is not None
        assert dto.data == core_source_data


def test_error_get_source_data_by_composite_index_either_input_is_none(
    app_initialization_container: ApplicationContainer,
    fake_source_data: SQLASourceData,
) -> None:
    sqla_source_data_repository = app_initialization_container.sqla_source_data_repository()

    sqla_source_data = fake_source_data

    dto = sqla_source_data_repository.get_source_data_by_composite_index(
        client_id=None, protocol=sqla_source_data.protocol, relative_path=sqla_source_data.relative_path  # type: ignore
    )

    assert dto
    assert dto.status == False
    assert dto.errorCode == -1
    assert dto.errorName == "ClientIDNotProvided"
    assert dto.errorType == "ClientIDNotProvided"

    dto = sqla_source_data_repository.get_source_data_by_composite_index(
        client_id=1, protocol=None, relative_path=sqla_source_data.relative_path  # type: ignore
    )

    assert dto
    assert dto.status == False
    assert dto.errorCode == -1
    assert dto.errorName == "ProtocolNotProvided"
    assert dto.errorType == "ProtocolNotProvided"

    dto = sqla_source_data_repository.get_source_data_by_composite_index(
        client_id=1, protocol=sqla_source_data.protocol, relative_path=None  # type: ignore
    )

    assert dto
    assert dto.status == False
    assert dto.errorCode == -1
    assert dto.errorName == "RelativePathNotProvided"
    assert dto.errorType == "RelativePathNotProvided"


def test_error_get_source_data_by_composite_index_either_not_found(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_client_with_source_data: SQLAClient,
    fake_source_data: SQLASourceData,
) -> None:
    sqla_source_data_repository = app_initialization_container.sqla_source_data_repository()

    sqla_client = fake_client_with_source_data

    with db_session() as session:
        # Control: there's actually something in the db
        sqla_client.save(session=session, flush=True)
        session.commit()

        # This goes without commiting
        sqla_source_data = fake_source_data

        dto = sqla_source_data_repository.get_source_data_by_composite_index(
            client_id=sqla_client.id, protocol=sqla_source_data.protocol, relative_path=sqla_source_data.relative_path
        )

        assert dto is not None
        assert dto.status == False
        assert dto.errorCode == -1
        assert dto.errorName == "SourceDataNotFound"
        assert dto.errorType == "SourceDataNotFound"
