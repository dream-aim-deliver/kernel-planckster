import random
from typing import List
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLAClient, SQLASourceData


def test_create_new_source_data(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_client_with_source_data_list: List[SQLAClient],
    fake_source_data: SQLASourceData,
) -> None:
    sqla_client_repository = app_initialization_container.sqla_client_repository()

    sqla_client_list = fake_client_with_source_data_list
    sqla_client = random.choice(sqla_client_list)

    sqla_source_data = fake_source_data
    source_data_name = sqla_source_data.name
    relative_path = sqla_source_data.relative_path
    protocol = sqla_source_data.protocol

    with db_session() as session:
        for client in sqla_client_list:
            session.add(client)
        session.commit()

        dto = sqla_client_repository.new_source_data(
            client_id=sqla_client.id,
            source_data_name=source_data_name,
            protocol=protocol,
            relative_path=relative_path,
        )

        assert dto.status == True

        # This combination of attributes should be unique
        queried_new_source_data_list = (
            session.query(SQLASourceData)
            .filter_by(
                client_id=sqla_client.id,
                protocol=sqla_source_data.protocol,
                relative_path=sqla_source_data.relative_path,
            )
            .all()
        )

        assert queried_new_source_data_list is not None
        assert len(queried_new_source_data_list) == 1

        queried_new_source_data = queried_new_source_data_list[0]
        assert isinstance(queried_new_source_data, SQLASourceData)
        assert queried_new_source_data.client_id == sqla_client.id
        assert queried_new_source_data.name == source_data_name
        assert queried_new_source_data.protocol == protocol
        assert queried_new_source_data.relative_path == relative_path
