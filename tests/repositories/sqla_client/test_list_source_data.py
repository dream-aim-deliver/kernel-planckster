import random
from typing import List
from faker import Faker
from lib.infrastructure.config.containers import ApplicationContainer

from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLAClient, SQLASourceData
from lib.infrastructure.repository.sqla.utils import convert_sqla_source_data_to_core_source_data


# TODO: this test works individually, but not when the whole test suit is run with pytest, as we have dangling source data from other tests
# See Issue #49
# def test_list_source_data_all_empty(
# app_initialization_container: ApplicationContainer,
# db_session: TDatabaseFactory,
# fake_knowledge_source_with_source_data: SQLAKnowledgeSource,
# ) -> None:
#   sqla_source_data_repository = app_initialization_container.sqla_source_data_repository()

#   with db_session() as session:
#   list_source_data_DTO = sqla_source_data_repository.list_source_data()

#   assert list_source_data_DTO is not None
#   assert list_source_data_DTO.status == True
#   assert list_source_data_DTO.data is not None
#   assert list_source_data_DTO.data == []


def test_list_source_data_by_client_id(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client_with_source_data_list: List[SQLAClient],
) -> None:
    sqla_client_repository = app_initialization_container.sqla_client_repository()

    sqla_client_list = fake_client_with_source_data_list

    sqla_client = random.choice(sqla_client_list)

    sqla_client_list.remove(sqla_client)
    all_other_source_data_list: List[SQLASourceData] = []
    for client in sqla_client_list:
        all_other_source_data_list.extend(client.source_data)

    sqla_source_data_list = sqla_client.source_data

    with db_session() as session:
        sqla_client.save(session=session, flush=True)
        for client in sqla_client_list:
            client.save(session=session, flush=True)
        session.commit()
        dto_source_data_list = sqla_client_repository.list_source_data(client_id=sqla_client.id)

        assert dto_source_data_list is not None
        assert dto_source_data_list.status == True
        assert dto_source_data_list.data is not None
        assert dto_source_data_list.data != []

        dto_sd_list = dto_source_data_list.data

        for sd in sqla_client.source_data:
            core_sd = convert_sqla_source_data_to_core_source_data(sd)
            assert core_sd in dto_sd_list

        for sd in all_other_source_data_list:
            # We don't want the source data from other knowledge sources to be listed in the DTO
            core_sd = convert_sqla_source_data_to_core_source_data(sd)
            assert core_sd not in dto_sd_list


def test_list_source_data_by_client_id_empty_source_data(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_client_with_source_data_list: List[SQLAClient],
) -> None:
    sqla_client_repository = app_initialization_container.sqla_client_repository()

    sqla_client_list = fake_client_with_source_data_list
    sqla_client = random.choice(sqla_client_list)
    sqla_client.source_data = []

    with db_session() as session:
        for client in sqla_client_list:
            client.save(session=session, flush=True)
        session.commit()

        list_source_data_DTO = sqla_client_repository.list_source_data(client_id=sqla_client.id)

        assert list_source_data_DTO is not None
        assert list_source_data_DTO.status == True
        assert list_source_data_DTO.data is not None
        assert list_source_data_DTO.data == []


def test_error_list_source_data_by_client_id_ks_not_found(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
) -> None:
    sqla_client_repository = app_initialization_container.sqla_client_repository()

    irrealistic_id = 999999999
    list_source_data_DTO = sqla_client_repository.list_source_data(client_id=irrealistic_id)

    assert list_source_data_DTO is not None
    assert list_source_data_DTO.status == False
    assert list_source_data_DTO.errorCode == -1
    assert list_source_data_DTO.errorType == "ClientNotFound"
