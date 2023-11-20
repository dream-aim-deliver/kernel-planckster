import random
from typing import List
from faker import Faker
from lib.core.dto.user_repository_dto import NewResearchContextDTO
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLALLM, SQLAKnowledgeSource, SQLAResearchContext, SQLAUser


def test_create_new_research_context(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_user: SQLAUser,
    fake_llm: SQLALLM,
    fake_knowledge_source_with_source_data_list: List[SQLAKnowledgeSource],
) -> None:
    sqla_user_repository = app_initialization_container.sqla_user_repository()

    user = fake_user
    llm = fake_llm
    knowledge_source_list = fake_knowledge_source_with_source_data_list
    rand_int_1 = random.randint(0, len(knowledge_source_list) - 1)
    knowledge_source = knowledge_source_list[rand_int_1]

    user_sid = user.sid
    llm_name = llm.llm_name

    research_context_title = fake.name()

    with db_session() as session:
        session.add(user)
        session.add(llm)
        for ks in knowledge_source_list:
            session.add(ks)
        session.commit()

        source_data_list = knowledge_source.source_data
        source_data_lfn_list = [source_data.lfn for source_data in source_data_list]
        source_data_id_list = [source_data.id for source_data in source_data_list]

    with db_session() as session:
        new_research_context_DTO: NewResearchContextDTO = sqla_user_repository.new_research_context(
            research_context_title=research_context_title,
            user_sid=user_sid,
            llm_name=llm_name,
            source_data_ids=source_data_id_list,
        )

        assert new_research_context_DTO.status == True

        assert new_research_context_DTO.research_context is not None
        assert new_research_context_DTO.llm is not None

        new_research_context_id = new_research_context_DTO.research_context.id
        new_research_context_llm = new_research_context_DTO.llm

        queried_new_research_context = session.get(SQLAResearchContext, new_research_context_id)

        assert queried_new_research_context is not None
        assert (
            queried_new_research_context.title
            == new_research_context_DTO.research_context.title
            == research_context_title
        )
        assert queried_new_research_context.llm_id == new_research_context_llm.id

        assert new_research_context_llm.llm_name == llm_name

        queried_new_research_context_source_data = queried_new_research_context.source_data

        queried_new_research_context_source_data_lfn_list = [sd.lfn for sd in queried_new_research_context_source_data]

        for source_data_lfn in source_data_lfn_list:
            assert source_data_lfn in queried_new_research_context_source_data_lfn_list


def test_error_new_research_context_research_context_title_is_None(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    sqla_user_repository = app_initialization_container.sqla_user_repository()

    research_context_title = None
    user_sid = "test"
    llm_name = "test"
    source_data_ids = [1, 2, 3]

    new_research_context_DTO: NewResearchContextDTO = sqla_user_repository.new_research_context(
        research_context_title=research_context_title,  # type: ignore
        user_sid=user_sid,
        llm_name=llm_name,
        source_data_ids=source_data_ids,
    )

    assert new_research_context_DTO.status == False
    assert new_research_context_DTO.errorCode == -1
    assert new_research_context_DTO.errorMessage == "Research context title cannot be None"
    assert new_research_context_DTO.errorName == "Research context title not provided"
    assert new_research_context_DTO.errorType == "ResearchContextTitleNotProvided"


def test_error_new_research_context_user_sid_is_None(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    sqla_user_repository = app_initialization_container.sqla_user_repository()

    research_context_title = "test"
    user_sid = None
    llm_name = "test"
    source_data_ids = [1, 2, 3]

    new_research_context_DTO: NewResearchContextDTO = sqla_user_repository.new_research_context(
        research_context_title=research_context_title,
        user_sid=user_sid,  # type: ignore
        llm_name=llm_name,
        source_data_ids=source_data_ids,
    )

    assert new_research_context_DTO.status == False
    assert new_research_context_DTO.errorCode == -1
    assert new_research_context_DTO.errorMessage == "User SID cannot be None"
    assert new_research_context_DTO.errorName == "User SID not provided"
    assert new_research_context_DTO.errorType == "UserSidNotProvided"


def test_error_new_research_context_llm_name_is_None(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    sqla_user_repository = app_initialization_container.sqla_user_repository()

    research_context_title = "test"
    user_sid = "test"
    llm_name = None
    source_data_ids = [1, 2, 3]

    new_research_context_DTO: NewResearchContextDTO = sqla_user_repository.new_research_context(
        research_context_title=research_context_title,
        user_sid=user_sid,
        llm_name=llm_name,  # type: ignore
        source_data_ids=source_data_ids,
    )

    assert new_research_context_DTO.status == False
    assert new_research_context_DTO.errorCode == -1
    assert new_research_context_DTO.errorMessage == "LLM name cannot be None"
    assert new_research_context_DTO.errorName == "LLM name not provided"
    assert new_research_context_DTO.errorType == "LLMNameNotProvided"


def test_error_new_research_context_user_sid_not_found(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_llm: SQLALLM,
) -> None:
    sqla_user_repository = app_initialization_container.sqla_user_repository()

    llm = fake_llm
    llm_name = llm.llm_name

    research_context_title = "test"
    user_sid = "test"
    source_data_ids = [1, 2, 3]

    with db_session() as session:
        session.add(llm)
        session.commit()

        new_research_context_DTO: NewResearchContextDTO = sqla_user_repository.new_research_context(
            research_context_title=research_context_title,
            user_sid=user_sid,
            llm_name=llm_name,
            source_data_ids=source_data_ids,
        )

        assert new_research_context_DTO.status == False
        assert new_research_context_DTO.errorCode == -1
        assert new_research_context_DTO.errorMessage == f"User with SID {user_sid} not found in the database"
        assert new_research_context_DTO.errorName == "User not found"
        assert new_research_context_DTO.errorType == "UserNotFound"


def test_error_new_research_context_llm_name_not_found(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_user: SQLAUser,
) -> None:
    sqla_user_repository = app_initialization_container.sqla_user_repository()

    user = fake_user
    user_sid = user.sid

    research_context_title = "test"
    llm_name = "test"
    source_data_ids = [1, 2, 3]

    with db_session() as session:
        session.add(user)
        session.commit()

        new_research_context_DTO: NewResearchContextDTO = sqla_user_repository.new_research_context(
            research_context_title=research_context_title,
            user_sid=user_sid,
            llm_name=llm_name,
            source_data_ids=source_data_ids,
        )

        assert new_research_context_DTO.status == False
        assert new_research_context_DTO.errorCode == -1
        assert new_research_context_DTO.errorMessage == f"LLM with name {llm_name} not found in the database"
        assert new_research_context_DTO.errorName == "LLM not found"
        assert new_research_context_DTO.errorType == "LLMNotFound"


def test_error_new_research_context_source_data_ids_not_found(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_user: SQLAUser,
    fake_llm: SQLALLM,
) -> None:
    sqla_user_repository = app_initialization_container.sqla_user_repository()

    user = fake_user
    llm = fake_llm
    user_sid = user.sid
    llm_name = llm.llm_name

    research_context_title = "test"
    source_data_ids = [999999999]

    with db_session() as session:
        session.add(user)
        session.add(llm)
        session.commit()

        new_research_context_DTO: NewResearchContextDTO = sqla_user_repository.new_research_context(
            research_context_title=research_context_title,
            user_sid=user_sid,
            llm_name=llm_name,
            source_data_ids=source_data_ids,
        )

        sqla_source_data_error_dict = {}
        for sd_id in source_data_ids:
            sqla_source_data_error_dict[f"ID {sd_id}"] = f"Source data not found in the database"

        error_message = f"Error with the following source data. Operation aborted.\n\n {sqla_source_data_error_dict}"

        assert new_research_context_DTO.status == False
        assert new_research_context_DTO.errorCode == -1
        assert new_research_context_DTO.errorMessage == error_message
        assert new_research_context_DTO.errorName == "Source data database errors"
        assert new_research_context_DTO.errorType == "SourceDataDatabaseErrors"
