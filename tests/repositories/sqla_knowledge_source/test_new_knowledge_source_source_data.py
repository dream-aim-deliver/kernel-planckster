import datetime
from typing import List
from faker import Faker
from lib.core.entity.models import SourceData
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLAKnowledgeSource, SQLASourceData
from lib.infrastructure.repository.sqla.utils import convert_sqla_source_data_to_core_source_data


def test_create_new_source_data(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_knowledge_source_with_source_data: SQLAKnowledgeSource,
    fake_source_data_list: List[SQLASourceData],
) -> None:
    sqla_knowledge_source_repository = app_initialization_container.sqla_knowledge_source_repository()

    knowledge_source = fake_knowledge_source_with_source_data
    knowledge_source_source = knowledge_source.source
    knowledge_source_content_metadata = knowledge_source.content_metadata

    sqla_source_data_list = fake_source_data_list

    core_source_data_list: List[SourceData] = []
    id_to_ignore = -1
    for sqla_source_datum in sqla_source_data_list:
        core_source_datum = SourceData(
            # The following 4 fields don't matter, will be ignored by the repository
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            deleted=False,
            deleted_at=None,
            # The ID field will be used to test that this is actually ignored by the repository
            id=id_to_ignore,
            # Only these one matter, which are the ones supposed to come from the primary side
            name=sqla_source_datum.name,
            type=sqla_source_datum.type,
            lfn=sqla_source_datum.lfn,
            protocol=sqla_source_datum.protocol,
            status=sqla_source_datum.status,
        )
        core_source_data_list.append(core_source_datum)

    source_data_lfn_list = [source_data.lfn for source_data in sqla_source_data_list]

    with db_session() as session:
        session.add(knowledge_source)
        session.commit()

    with db_session() as session:
        queried_sqla_knowledge_source = (
            session.query(SQLAKnowledgeSource)
            .filter_by(source=knowledge_source_source)
            .filter_by(content_metadata=knowledge_source_content_metadata)
            .first()
        )
        assert queried_sqla_knowledge_source is not None

        knowledge_source_id = queried_sqla_knowledge_source.id
        new_source_data_DTO = sqla_knowledge_source_repository.new_source_data(
            knowledge_source_id=knowledge_source_id, source_data_list=core_source_data_list
        )

        assert new_source_data_DTO.status == True

        queried_new_source_data = (
            session.query(SQLASourceData).filter(SQLASourceData.lfn.in_(source_data_lfn_list)).all()
        )

        assert queried_new_source_data is not None
        assert queried_new_source_data != []

        for queried_source_datum in queried_new_source_data:
            assert isinstance(queried_source_datum, SQLASourceData)
            assert queried_source_datum.knowledge_source_id == knowledge_source_id

        queried_new_source_data_lfns = [queried_source_datum.lfn for queried_source_datum in queried_new_source_data]

        for source_datum_lfn in source_data_lfn_list:
            assert source_datum_lfn in queried_new_source_data_lfns

        queried_new_source_data_ids = [queried_source_datum.id for queried_source_datum in queried_new_source_data]

        for source_datum_id in queried_new_source_data_ids:
            assert source_datum_id != id_to_ignore


def FIRST_FIX_TODO_IN_SQLA_REPOSITORY_test_half_error_create_new_source_data_duplicate_lfns(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_knowledge_source_with_source_data: SQLAKnowledgeSource,
    fake_source_data_list: List[SQLASourceData],
) -> None:
    sqla_knowledge_source_repository = app_initialization_container.sqla_knowledge_source_repository()

    knowledge_source = fake_knowledge_source_with_source_data
    knowledge_source_source = knowledge_source.source
    knowledge_source_content_metadata = knowledge_source.content_metadata

    fake_sqla_source_data_list = fake_source_data_list
    sqla_source_data_list = []
    # Same in purpose
    sqla_source_data_list.append(fake_sqla_source_data_list[0])
    sqla_source_data_list.append(fake_sqla_source_data_list[0])
    sqla_source_data_list.append(fake_sqla_source_data_list[1])
    sqla_source_data_list.append(fake_sqla_source_data_list[1])
    sqla_source_data_list.append(fake_sqla_source_data_list[2])
    sqla_source_data_list.append(fake_sqla_source_data_list[2])

    core_source_data_list: List[SourceData] = []
    for sqla_source_datum in sqla_source_data_list:
        core_source_datum = SourceData(
            # The following 5 fields don't matter, will be ignored by the repository
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            deleted=False,
            deleted_at=None,
            id=1,
            # Only these one matter, which are the ones supposed to come from the primary side
            name=sqla_source_datum.name,
            type=sqla_source_datum.type,
            lfn=sqla_source_datum.lfn,
            protocol=sqla_source_datum.protocol,
            status=sqla_source_datum.status,
        )
        core_source_data_list.append(core_source_datum)

    source_data_lfn_list = [source_data.lfn for source_data in sqla_source_data_list]

    with db_session() as session:
        session.add(knowledge_source)
        session.commit()

    with db_session() as session:
        queried_sqla_knowledge_source = (
            session.query(SQLAKnowledgeSource)
            .filter_by(source=knowledge_source_source)
            .filter_by(content_metadata=knowledge_source_content_metadata)
            .first()
        )
        assert queried_sqla_knowledge_source is not None

        queried_sqla_knowledge_source_id = queried_sqla_knowledge_source.id

        knowledge_source_id = queried_sqla_knowledge_source.id
        new_source_data_DTO = sqla_knowledge_source_repository.new_source_data(
            knowledge_source_id=knowledge_source_id, source_data_list=core_source_data_list
        )

        assert new_source_data_DTO.status == True
        assert new_source_data_DTO.errorCode == -1
        assert new_source_data_DTO.errorName == "Success but Source Data creation error for some source data"
        assert new_source_data_DTO.errorType == "SuccesButSourceDataCreationError"

    with db_session() as session:
        queried_sqla_knowledge_source = session.get(SQLAKnowledgeSource, queried_sqla_knowledge_source_id)
        assert queried_sqla_knowledge_source is not None

        queried_sqla_knowledge_source_source_data_list = queried_sqla_knowledge_source.source_data
        queried_sqla_knowledge_source_source_data_lfns = [
            queried_sqla_source_datum.lfn
            for queried_sqla_source_datum in queried_sqla_knowledge_source_source_data_list
        ]

        for sqla_source_datum_lfn in source_data_lfn_list:
            assert sqla_source_datum_lfn in queried_sqla_knowledge_source_source_data_lfns
