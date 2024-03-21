import random
from typing import List
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLAKnowledgeSource, SQLASourceData
from lib.infrastructure.repository.sqla.utils import convert_sqla_lfn_to_core_lfn
from tests.conftest import db_session


def test_get_source_data_by_lfn(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_knowledge_source_with_source_data_list: List[SQLAKnowledgeSource],
) -> None:
    sqla_source_data_repository = app_initialization_container.sqla_source_data_repository()

    knowledge_sources = fake_knowledge_source_with_source_data_list

    sqla_source_data_list: List[SQLASourceData] = []
    for ks in knowledge_sources:
        sqla_source_data_list.extend(ks.source_data)

    sqla_source_data_lfns_list = [sd.lfn for sd in sqla_source_data_list]

    rand_i = random.randint(0, len(sqla_source_data_lfns_list))
    sqla_lfn = sqla_source_data_lfns_list[rand_i]
    core_lfn = convert_sqla_lfn_to_core_lfn(sqla_lfn)

    with db_session() as session:
        for ks in knowledge_sources:
            ks.save(session=session, flush=True)
        session.commit()

        dto = sqla_source_data_repository.get_source_data_by_lfn(core_lfn)

        assert dto is not None
        assert dto.status == True
        assert dto.data is not None
        assert core_lfn == dto.data.lfn


def test_error_get_source_data_by_lfn_input_is_none(
    app_initialization_container: ApplicationContainer,
) -> None:
    sqla_source_data_repository = app_initialization_container.sqla_source_data_repository()

    dto = sqla_source_data_repository.get_source_data_by_lfn(lfn=None)  # type: ignore

    assert dto
    assert dto.status == False
    assert dto.errorCode == -1
    assert dto.errorMessage == "LFN cannot be None"
    assert dto.errorName == "LFNNotProvided"
    assert dto.errorType == "LFNNotProvided"


def test_error_get_source_data_by_lfn_not_found(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_knowledge_source_with_source_data_list: List[SQLAKnowledgeSource],
    fake_source_data: SQLASourceData,
) -> None:
    sqla_source_data_repository = app_initialization_container.sqla_source_data_repository()

    knowledge_sources = fake_knowledge_source_with_source_data_list

    with db_session() as session:
        # Control: there's actually something in the db
        for ks in knowledge_sources:
            ks.save(session=session, flush=True)
        session.commit()

        # These go without commiting
        sqla_source_data = fake_source_data
        sqla_lfn = sqla_source_data.lfn
        core_lfn = convert_sqla_lfn_to_core_lfn(sqla_lfn)

        dto = sqla_source_data_repository.get_source_data_by_lfn(core_lfn)

        assert dto is not None
        assert dto.status == False
        assert dto.errorCode == -1
        assert dto.errorMessage == f"Source Data with LFN {core_lfn.to_json()} not found in the database"
        assert dto.errorName == "SourceDataNotFound"
        assert dto.errorType == "SourceDataNotFound"
