import random
from typing import List
import uuid
from faker import Faker
from lib.core.dto.client_repository_dto import NewResearchContextDTO
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLALLM, SQLAResearchContext, SQLAClient


def test_create_new_research_context(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_llm: SQLALLM,
    fake_client_with_source_data_list: List[SQLAClient],
) -> None:
    sqla_client_repository = app_initialization_container.sqla_client_repository()

    llm = fake_llm
    client_list = fake_client_with_source_data_list
    client = random.choice(client_list)

    client_sub = client.sub
    llm_name = llm.llm_name

    research_context_title = fake.name()
    research_context_description = fake.text()

    with db_session() as session:
        session.add(llm)
        for client in client_list:
            session.add(client)
        session.commit()

        source_data_list = client.source_data
        source_data_id_list = [source_data.id for source_data in source_data_list]

    with db_session() as session:
        new_research_context_DTO: NewResearchContextDTO = sqla_client_repository.new_research_context(
            research_context_title=research_context_title,
            research_context_description=research_context_description,
            client_sub=client_sub,
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
        assert (
            queried_new_research_context.description
            == new_research_context_DTO.research_context.description
            == research_context_description
        )
        assert queried_new_research_context.llm_id == new_research_context_llm.id

        assert new_research_context_llm.llm_name == llm_name

        queried_new_research_context_source_data = queried_new_research_context.source_data

        assert len(queried_new_research_context_source_data) == len(source_data_id_list)

        for source_data in queried_new_research_context_source_data:
            assert source_data.id in source_data_id_list


def test_error_new_research_context_research_context_title_is_None(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    sqla_client_repository = app_initialization_container.sqla_client_repository()

    research_context_title = None
    research_context_description = "Test description"
    client_sub = "test"
    llm_name = "test"
    source_data_ids = [1, 2, 3]

    new_research_context_DTO: NewResearchContextDTO = sqla_client_repository.new_research_context(
        research_context_title=research_context_title,
        research_context_description=research_context_description,
        client_sub=client_sub,
        llm_name=llm_name,
        source_data_ids=source_data_ids,
    )

    assert new_research_context_DTO.status == False
    assert new_research_context_DTO.errorCode == -1
    assert new_research_context_DTO.errorName == "Research context title not provided"
    assert new_research_context_DTO.errorType == "ResearchContextTitleNotProvided"


def test_error_new_research_context_description_is_None(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    sqla_client_repository = app_initialization_container.sqla_client_repository()

    research_context_title = "test"
    research_context_description = None
    client_sub = "test"
    llm_name = "test"
    source_data_ids = [1, 2, 3]

    new_research_context_DTO: NewResearchContextDTO = sqla_client_repository.new_research_context(
        research_context_title=research_context_title,
        research_context_description=research_context_description,
        client_sub=client_sub,
        llm_name=llm_name,
        source_data_ids=source_data_ids,
    )

    assert new_research_context_DTO.status == False
    assert new_research_context_DTO.errorCode == -1
    assert new_research_context_DTO.errorName == "Research context description not provided"
    assert new_research_context_DTO.errorType == "ResearchContextDescriptionNotProvided"


def test_error_new_research_context_client_sub_is_None(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    sqla_client_repository = app_initialization_container.sqla_client_repository()

    research_context_title = "test"
    research_context_description = "Test description"
    client_sub = None
    llm_name = "test"
    source_data_ids = [1, 2, 3]

    new_research_context_DTO: NewResearchContextDTO = sqla_client_repository.new_research_context(
        research_context_title=research_context_title,
        research_context_description=research_context_description,
        client_sub=client_sub,
        llm_name=llm_name,
        source_data_ids=source_data_ids,
    )

    assert new_research_context_DTO.status == False
    assert new_research_context_DTO.errorCode == -1
    assert new_research_context_DTO.errorName == "Client SUB not provided"
    assert new_research_context_DTO.errorType == "ClientSubNotProvided"


def test_error_new_research_context_llm_name_is_None(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    sqla_client_repository = app_initialization_container.sqla_client_repository()

    research_context_title = "test"
    research_context_description = "Test description"
    client_sub = "test"
    llm_name = None
    source_data_ids = [1, 2, 3]

    new_research_context_DTO: NewResearchContextDTO = sqla_client_repository.new_research_context(
        research_context_title=research_context_title,
        research_context_description=research_context_description,
        client_sub=client_sub,
        llm_name=llm_name,
        source_data_ids=source_data_ids,
    )

    assert new_research_context_DTO.status == False
    assert new_research_context_DTO.errorCode == -1
    assert new_research_context_DTO.errorName == "LLM name not provided"
    assert new_research_context_DTO.errorType == "LLMNameNotProvided"


def test_error_new_research_context_client_sub_not_found(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_llm: SQLALLM,
) -> None:
    sqla_client_repository = app_initialization_container.sqla_client_repository()

    llm = fake_llm
    llm_name = llm.llm_name

    research_context_title = "test"
    research_context_description = "Test description"
    client_sub = f"test-{uuid.uuid4()}"
    source_data_ids = [1, 2, 3]

    with db_session() as session:
        session.add(llm)
        session.commit()

        new_research_context_DTO: NewResearchContextDTO = sqla_client_repository.new_research_context(
            research_context_title=research_context_title,
            research_context_description=research_context_description,
            client_sub=client_sub,
            llm_name=llm_name,
            source_data_ids=source_data_ids,
        )

        assert new_research_context_DTO.status == False
        assert new_research_context_DTO.errorCode == -1
        assert new_research_context_DTO.errorName == "Client not found"
        assert new_research_context_DTO.errorType == "ClientNotFound"


def test_error_new_research_context_llm_name_not_found(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_client: SQLAClient,
) -> None:
    sqla_client_repository = app_initialization_container.sqla_client_repository()

    client = fake_client
    client_sub = client.sub

    research_context_title = "test"
    research_context_description = "Test description"
    llm_name = f"test-{uuid.uuid4()}"
    source_data_ids = [1, 2, 3]

    with db_session() as session:
        session.add(client)
        session.commit()

        new_research_context_DTO: NewResearchContextDTO = sqla_client_repository.new_research_context(
            research_context_title=research_context_title,
            research_context_description=research_context_description,
            client_sub=client_sub,
            llm_name=llm_name,
            source_data_ids=source_data_ids,
        )

        assert new_research_context_DTO.status == False
        assert new_research_context_DTO.errorCode == -1
        assert new_research_context_DTO.errorName == "LLM not found"
        assert new_research_context_DTO.errorType == "LLMNotFound"


def test_error_new_research_context_source_data_ids_not_found(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_client: SQLAClient,
    fake_llm: SQLALLM,
) -> None:
    sqla_client_repository = app_initialization_container.sqla_client_repository()

    client = fake_client
    llm = fake_llm
    client_sub = client.sub
    llm_name = llm.llm_name

    research_context_title = "test"
    research_context_description = "Test description"
    source_data_ids = [999999999]

    with db_session() as session:
        session.add(client)
        session.add(llm)
        session.commit()

        new_research_context_DTO: NewResearchContextDTO = sqla_client_repository.new_research_context(
            research_context_title=research_context_title,
            research_context_description=research_context_description,
            client_sub=client_sub,
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
