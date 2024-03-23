import random
from typing import List
from faker import Faker
from lib.core.dto.source_data_repository_dto import ListSourceDataDTO
from lib.infrastructure.config.containers import ApplicationContainer

from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLAKnowledgeSource, SQLASourceData


def test_list_source_data_all(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_knowledge_source_with_source_data_list: List[SQLAKnowledgeSource],
) -> None:
    sqla_source_data_repository = app_initialization_container.sqla_source_data_repository()

    knowledge_sources = fake_knowledge_source_with_source_data_list

    sqla_source_data_list: List[SQLASourceData] = []
    for ks in knowledge_sources:
        sqla_source_data_list.extend(ks.source_data)

    sqla_source_data_lfns_list = [sd.lfn for sd in sqla_source_data_list]

    with db_session() as session:
        for ks in knowledge_sources:
            ks.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        dto_source_data_list = sqla_source_data_repository.list_source_data()

        assert dto_source_data_list is not None
        assert dto_source_data_list.status == True
        assert dto_source_data_list.data is not None
        assert dto_source_data_list.data != []

        dto_source_data_lfns_list = [sd.lfn.to_json() for sd in dto_source_data_list.data]

        for sd_lfn in sqla_source_data_lfns_list:
            assert sd_lfn in dto_source_data_lfns_list


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


def test_list_source_data_by_knowledge_source_id(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_knowledge_source_with_source_data_list: List[SQLAKnowledgeSource],
) -> None:
    sqla_source_data_repository = app_initialization_container.sqla_source_data_repository()

    knowledge_sources = fake_knowledge_source_with_source_data_list

    knowledge_source = random.choice(knowledge_sources)

    knowledge_sources.remove(knowledge_source)
    all_other_source_data_list: List[SQLASourceData] = []
    for ks in knowledge_sources:
        all_other_source_data_list.extend(ks.source_data)
    all_other_source_data_lfn_list = [sd.lfn for sd in all_other_source_data_list]

    sqla_source_data_list = knowledge_source.source_data
    sqla_source_data_lfns_list = [sd.lfn for sd in sqla_source_data_list]

    with db_session() as session:
        knowledge_source.save(session=session, flush=True)
        for ks in knowledge_sources:
            ks.save(session=session, flush=True)
        session.commit()
        knowledge_source_id = knowledge_source.id

    with db_session() as session:
        dto_source_data_list = sqla_source_data_repository.list_source_data(knowledge_source_id=knowledge_source_id)

        assert dto_source_data_list is not None
        assert dto_source_data_list.status == True
        assert dto_source_data_list.data is not None
        assert dto_source_data_list.data != []

        dto_lfn_list = [sd.lfn.to_json() for sd in dto_source_data_list.data]

        for sd_lfn in sqla_source_data_lfns_list:
            assert sd_lfn in dto_lfn_list

        for sd_lfn in all_other_source_data_lfn_list:
            # We don't want the source data from other knowledge sources to be listed in the DTO
            assert sd_lfn not in dto_lfn_list


def test_list_source_data_by_knowledge_source_id_empty_source_data(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_knowledge_source_with_source_data_list: List[SQLAKnowledgeSource],
) -> None:
    sqla_source_data_repository = app_initialization_container.sqla_source_data_repository()

    knowledge_sources = fake_knowledge_source_with_source_data_list
    knowledge_source = random.choice(knowledge_sources)
    knowledge_source.source_data = []

    with db_session() as session:
        for ks in knowledge_sources:
            ks.save(session=session, flush=True)
        session.commit()
        knowledge_source_id = knowledge_source.id

    with db_session() as session:
        list_source_data_DTO: ListSourceDataDTO = sqla_source_data_repository.list_source_data(
            knowledge_source_id=knowledge_source.id
        )

        assert list_source_data_DTO is not None
        assert list_source_data_DTO.status == True
        assert list_source_data_DTO.data is not None
        assert list_source_data_DTO.data == []


def test_error_list_source_data_by_knowledge_source_id_ks_not_found(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
) -> None:
    sqla_source_data_repository = app_initialization_container.sqla_source_data_repository()

    irrealistic_id = 99999999
    list_source_data_DTO: ListSourceDataDTO = sqla_source_data_repository.list_source_data(
        knowledge_source_id=irrealistic_id
    )

    assert list_source_data_DTO is not None
    assert list_source_data_DTO.status == False
    assert list_source_data_DTO.errorCode == -1
    assert list_source_data_DTO.errorMessage == f"Knowledge source with ID {irrealistic_id} not found in the database"
    assert list_source_data_DTO.errorName == "KnowledgeSourceNotFound"
    assert list_source_data_DTO.errorType == "KnowledgeSourceNotFound"
