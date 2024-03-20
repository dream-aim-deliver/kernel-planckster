import datetime
from typing import List
from lib.core.entity.models import LFN, SourceData
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLAKnowledgeSource, SQLASourceData


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
    sqla_source_data = sqla_source_data_list[0]
    lfn = LFN.from_json(sqla_source_data.lfn)

    id_to_ignore = -1
    core_source_data = SourceData(
        # The following 4 fields don't matter, will be ignored by the repository
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        deleted=False,
        deleted_at=None,
        # The ID field will be used to test that this is actually ignored by the repository
        id=id_to_ignore,
        # Only these one matter, which are the ones supposed to come from the primary side
        name=sqla_source_data.name,
        type=sqla_source_data.type,
        lfn=lfn,
        status=sqla_source_data.status,
    )

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
            knowledge_source_id=knowledge_source_id, source_data=core_source_data
        )

        assert new_source_data_DTO.status == True

        queried_new_source_data_list = (
            session.query(SQLASourceData).filter(SQLASourceData.lfn.in_([sqla_source_data.lfn])).all()
        )

        assert queried_new_source_data_list is not None
        assert len(queried_new_source_data_list) == 1

        queried_new_source_data = queried_new_source_data_list[0]
        assert isinstance(queried_new_source_data, SQLASourceData)
        assert queried_new_source_data.knowledge_source_id == knowledge_source_id
        assert sqla_source_data.lfn == queried_new_source_data.lfn
        assert queried_new_source_data.id != id_to_ignore
