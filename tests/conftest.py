from contextlib import _GeneratorContextManager
import datetime
from importlib import metadata
import os
import random
from typing import Annotated, Callable, Generator, List, Protocol, Tuple
from faker import Faker
from faker.proxy import UniqueProxy
from fastapi import FastAPI
from fastapi.testclient import TestClient
import psycopg2
import pytest
import yaml
import lib
from lib.core.entity.models import KnowledgeSourceEnum, ProtocolEnum, SourceDataStatusEnum
from lib.infrastructure.config.containers import ApplicationContainer
from alembic.config import Config
from alembic import command
from sqlalchemy.orm import Session

from lib.infrastructure.repository.sqla.database import Database, TDatabaseFactory
from lib.infrastructure.repository.sqla.models import (
    SQLACitation,
    SQLAConversation,
    SQLAKnowledgeSource,
    SQLAMessageBase,
    SQLAMessageQuery,
    SQLAMessageResponse,
    SQLAResearchContext,
    SQLASourceData,
    SQLAUser,
)
from tests.fixtures.factory.sqla_model_factory import SQLATemporaryModelFactory


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig: Annotated[pytest.Config, pytest.fixture]) -> str:
    return os.path.join(str(pytestconfig.rootdir), "tests", "docker-compose.yml")  # type: ignore


# set autouse=True to automatically inject the postgres into all tests
@pytest.fixture(scope="session")
def start_docker_services(
    request: pytest.FixtureRequest,
    docker_services: pytest.fixture,  # type: ignore
) -> None:
    """Ensure that a postgres container is running before running tests"""

    def is_responsive(rdbms: dict[str, str]) -> bool:
        try:
            conn = psycopg2.connect(
                host=rdbms["host"],
                database=rdbms["database"],
                port=rdbms["port"],
                user=rdbms["username"],
                password=rdbms["password"],
            )
            return True
        except Exception as e:
            return False

    try:
        config_yaml = os.path.join(str(request.config.rootdir), "config.yaml")  # type: ignore
        with open(config_yaml, "r") as f:
            config = yaml.safe_load(f)

        rdbms_config = config["rdbms"]
        rdbms = {
            "host": os.getenv("KP_RDBMS_HOST", rdbms_config["host"].split(":"[-1][-1])),
            "port": os.getenv("KP_RDBMS_PORT", rdbms_config["port"].split(":"[-1][-1])),
            "database": os.getenv("KP_RDBMS_DBNAME", rdbms_config["database"].split(":"[-1][-1])),
            "username": os.getenv("KP_RDBMS_USERNAME", rdbms_config["username"].split(":"[-1][-1])),
            "password": os.getenv("KP_RDBMS_PASSWORD", rdbms_config["password"].split(":"[-1][-1])),
        }
        docker_services.wait_until_responsive(timeout=60.0, pause=0.1, check=lambda: is_responsive(rdbms))  # type: ignore
    except Exception as e:
        pytest.fail(f"Failed to start postgres container, error: {e}")


# set autouse=True to automatically inject the container into all tests
@pytest.fixture(scope="session")
def app_initialization_container(start_docker_services: None) -> ApplicationContainer:
    container = ApplicationContainer()
    print(container.config())
    container.wire(modules=[lib])
    return container


@pytest.fixture(scope="session")
def app_raw_db(app_initialization_container: ApplicationContainer) -> Database:
    return app_initialization_container.db()


@pytest.fixture(scope="session")
def run_rdbms_migrations(request: pytest.FixtureRequest, app_raw_db: Database) -> None:
    """Run alembic migrations before running tests and tear them down after"""
    alembic_ini_path = os.path.join(str(request.config.rootdir), "alembic.ini")  # type: ignore
    alembic_cfg = Config(alembic_ini_path)

    alembic_scripts_path = os.path.join(str(request.config.rootdir), "alembic")  # type: ignore
    alembic_cfg.set_main_option("script_location", alembic_scripts_path)

    alembic_cfg.set_main_option("sqlalchemy.url", app_raw_db.url)

    try:
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        pytest.fail("Failed to run migrations, error: {e}")
    # request.addfinalizer(lambda: command.downgrade(alembic_cfg, "base"))


@pytest.fixture(scope="session")
def app_migrated_db(run_rdbms_migrations: None, app_raw_db: Database) -> Database:
    """Create a new database session for each test"""
    return app_raw_db


@pytest.fixture(scope="function")
def db_session(app_migrated_db: Database) -> Generator[Callable[[], _GeneratorContextManager[Session]], None, None]:
    """Create a new database session for each test"""
    yield app_migrated_db.session


@pytest.fixture(scope="function")
def app_container(app_migrated_db: Database) -> ApplicationContainer:
    container = ApplicationContainer()
    container.wire(modules=[lib])
    return container


@pytest.fixture(scope="function")
def server(app_container: None) -> FastAPI:
    from lib.infrastructure.rest.main import create_app

    app = create_app()
    return app


@pytest.fixture(scope="function")
def client(server: FastAPI) -> TestClient:
    test_client = TestClient(server)
    return test_client


@pytest.fixture(scope="function")
def fake() -> UniqueProxy:
    return Faker().unique


@pytest.fixture
def sqla_temp_model_factory(
    db_session: TDatabaseFactory,
) -> Generator[SQLATemporaryModelFactory, None, None]:
    session: Session
    with db_session() as s:
        session = s
    with SQLATemporaryModelFactory(session) as factory:
        yield factory


@pytest.fixture(scope="function")
def fake_kp_datetimes() -> Tuple[str, str, bool, str]:
    fake = Faker().unique

    dt1 = fake.date_time_between(start_date="-5y", end_date="-1m")

    dt2 = fake.date_time_between_dates(
        datetime_start=dt1, datetime_end=datetime.datetime.now() - datetime.timedelta(weeks=1)
    )

    dt3 = fake.date_time_between_dates(datetime_start=dt2, datetime_end=datetime.datetime.now())

    created_at = dt1.strftime("%Y-%m-%d %H:%M:%S")
    updated_at = dt2.strftime("%Y-%m-%d %H:%M:%S")
    deleted = Faker().boolean()
    deleted_at = dt3.strftime("%Y-%m-%d %H:%M:%S") if deleted else None

    return created_at, updated_at, deleted, deleted_at


def message_query() -> SQLAMessageQuery:
    fake = Faker().unique

    dt1 = fake.date_time_between(start_date="-8y", end_date="-1m")

    return SQLAMessageQuery(
        content=fake.text(max_nb_chars=70)[:-1] + "?",
        timestamp=dt1,
    )


@pytest.fixture(scope="function")
def fake_message_query() -> SQLAMessageQuery:
    return message_query()


def message_response() -> SQLAMessageResponse:
    fake = Faker().unique

    dt1 = fake.date_time_between(start_date="-8y", end_date="-1m")

    return SQLAMessageResponse(
        content=fake.text(max_nb_chars=70)[:-1],
        timestamp=dt1,
    )


@pytest.fixture(scope="function")
def fake_message_response() -> SQLAMessageResponse:
    return message_response()


def message_pair() -> Tuple[SQLAMessageQuery, SQLAMessageResponse]:
    fake = Faker().unique

    dt1 = fake.date_time_between(start_date="-8y", end_date="-1m")

    dt2 = fake.date_time_between_dates(datetime_start=dt1, datetime_end=datetime.datetime.now())

    message_query = SQLAMessageQuery(
        content=fake.text(max_nb_chars=70)[:-1] + "?",
        timestamp=dt1,
    )
    message_response = SQLAMessageResponse(
        content=fake.text(max_nb_chars=70)[:-1],
        timestamp=dt2,
    )

    return message_query, message_response


@pytest.fixture(scope="function")
def fake_message_pair() -> Tuple[SQLAMessageQuery, SQLAMessageResponse]:
    return message_pair()


TMessagePair = Tuple[SQLAMessageQuery, SQLAMessageResponse]


def conversation(number_of_message_pairs: int = 1) -> SQLAConversation:
    """
    Creates a conversation with a title and a list of messages
    The messages are created by calling message_pair() number_of_message_pairs times, which will create a list alternating a SQLAMessageQuery and a SQLAMessageResponse
    """

    fake = Faker().unique

    fake_title = fake.text(max_nb_chars=70)

    nested_tup = tuple(message_pair() for _ in range(number_of_message_pairs + 1))

    fake_messages_init = tuple(message for tup in nested_tup for message in tup)
    fake_messages: List[SQLAMessageBase] = list(fake_messages_init)

    return SQLAConversation(
        title=fake_title,
        messages=fake_messages,
    )


@pytest.fixture(scope="function")
def fake_conversation() -> SQLAConversation:
    return conversation()


def research_context(
    number_of_conversations: int = 4,
    up_bound_message_pairs_per_conversation: int = 5,
) -> SQLAResearchContext:
    """
    Creates a research context with a title and a list of conversations
    The conversations are created by calling conversation() number_of_conversations times, with an upper bound of maximum possible message pairs per conversation of up_bound_messages_per_conversation
    """
    fake = Faker().unique

    fake_title = fake.name()

    fake_conversations_init = tuple(
        conversation(random.randrange(1, up_bound_message_pairs_per_conversation + 1))
        for _ in range(number_of_conversations + 1)
    )
    fake_conversations = list(fake_conversations_init)

    return SQLAResearchContext(
        title=fake_title,
        conversations=fake_conversations,
    )


@pytest.fixture(scope="function")
def fake_research_context() -> SQLAResearchContext:
    return research_context()


def user() -> SQLAUser:
    fake = Faker().unique

    fake_sid = fake.name()

    return SQLAUser(
        sid=fake_sid,
    )


@pytest.fixture(scope="function")
def fake_user() -> SQLAUser:
    return user()


def user_with_conversation(number_of_research_contexts: int = 2) -> SQLAUser:
    fake = Faker().unique

    fake_sid = fake.name()

    fake_research_contexts_init = tuple(research_context() for _ in range(number_of_research_contexts + 1))
    fake_research_contexts = list(fake_research_contexts_init)
    #    fake_research_context = research_context()

    return SQLAUser(
        sid=fake_sid,
        research_contexts=fake_research_contexts,
    )


@pytest.fixture(scope="function")
def fake_user_with_conversation() -> SQLAUser:
    return user_with_conversation()


def source_data() -> SQLASourceData:
    fake = Faker().unique

    protocols = [
        attr_name.__str__().lower() for attr_name in vars(ProtocolEnum) if not attr_name.__str__().startswith("_")
    ]
    knowledge_sources = [
        attr_name.__str__().lower()
        for attr_name in vars(KnowledgeSourceEnum)
        if not attr_name.__str__().startswith("_")
    ]

    sd_protocol_choice: str = random.choice(protocols)
    sd_protocol = ProtocolEnum(sd_protocol_choice)
    sd_host = fake.domain_name()
    sd_port = fake.port_number()
    sd_minio_bucket = fake.name()
    sd_tracer_id = random.randint(1, 1000000000)
    sd_knowledge_source_choice: str = random.choice(knowledge_sources)
    sd_job_id = random.randint(1, 1000000000)

    sd_filename = fake.file_name()
    sd_name = sd_filename.split(".")[0]
    sd_type = sd_filename.split(".")[1]
    sd_relative_path = fake.file_path(depth=3).split(".")[0] + "/" + sd_filename

    sd_lfn = f"{sd_protocol_choice}://{sd_host}:{sd_port}/{sd_minio_bucket}/{sd_tracer_id}/{sd_knowledge_source_choice}/{sd_job_id}{sd_relative_path}"

    statuses = [
        attr_name.__str__().lower()
        for attr_name in vars(SourceDataStatusEnum)
        if not attr_name.__str__().startswith("_")
    ]
    sd_status_choice: str = random.choice(statuses)
    sd_status = SourceDataStatusEnum(sd_status_choice)

    return SQLASourceData(name=sd_name, type=sd_type, lfn=sd_lfn, protocol=sd_protocol, status=sd_status)


@pytest.fixture(scope="function")
def fake_source_data() -> SQLASourceData:
    return source_data()


@pytest.fixture(scope="function")
def fake_source_data_list() -> List[SQLASourceData]:
    return [source_data() for _ in range(10)]


def knowledge_source_with_source_data(number_of_source_data: int = 3) -> SQLAKnowledgeSource:
    fake = Faker().unique

    ks_enums = [
        attr_name.__str__().lower()
        for attr_name in vars(KnowledgeSourceEnum)
        if not attr_name.__str__().startswith("_")
    ]

    ks_source_choice: str = random.choice(ks_enums)
    ks_source = KnowledgeSourceEnum(ks_source_choice)

    fake_metadata = fake.text(max_nb_chars=70)

    fake_source_data_init = tuple(source_data() for _ in range(number_of_source_data + 1))
    fake_source_data = list(fake_source_data_init)

    return SQLAKnowledgeSource(
        source=ks_source,
        content_metadata=fake_metadata,
        source_data=fake_source_data,
    )


@pytest.fixture(scope="function")
def fake_knowledge_source_with_source_data() -> SQLAKnowledgeSource:
    return knowledge_source_with_source_data()


@pytest.fixture(scope="function")
def fake_knowledge_source_with_source_data_list() -> List[SQLAKnowledgeSource]:
    return [knowledge_source_with_source_data() for _ in range(10)]


def citation() -> SQLACitation:
    fake = Faker().unique

    fake_metadata = fake.text(max_nb_chars=70)

    return SQLACitation(
        citation_metadata=fake_metadata,
    )


@pytest.fixture(scope="function")
def fake_citation() -> SQLACitation:
    return citation()


@pytest.fixture(scope="function")
def fake_citations() -> List[SQLACitation]:
    return [citation() for _ in range(20)]
