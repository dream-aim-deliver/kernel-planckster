from contextlib import _GeneratorContextManager
import datetime
import os
import random
import tempfile
from typing import Annotated, Callable, Generator, List, Tuple
import uuid
from faker import Faker
from faker.proxy import UniqueProxy
from fastapi import FastAPI
from fastapi.testclient import TestClient
import psycopg2
import pytest
import yaml
import lib
from lib.core.entity.models import (
    ProtocolEnum,
    SourceData,
    SourceDataStatusEnum,
    MessageContentTypeEnum,
)
from lib.infrastructure.config.containers import ApplicationContainer
from alembic.config import Config
from alembic import command
from sqlalchemy.orm import Session

from lib.infrastructure.repository.minio.minio_object_store import MinIOObjectStore
from lib.infrastructure.repository.sqla.database import Database, TDatabaseFactory
from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLACitation,
    SQLAConversation,
    SQLAMessageBase,
    SQLAUserMessage,
    SQLAAgentMessage,
    SQLAMessageContent,
    SQLAResearchContext,
    SQLASourceData,
    SQLAClient,
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
    """Ensure that a postgres container and a minio container are running before running tests"""

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

    def is_object_store_responsive(object_store_conf: dict[str, str]) -> bool:
        try:
            object_store = MinIOObjectStore(
                host=object_store_conf["host"],
                port=object_store_conf["port"],
                access_key=object_store_conf["access_key"],
                secret_key=object_store_conf["secret_key"],
                signed_url_expiry=1,
            )
            return object_store.ping()
        except Exception as e:
            return False

    try:
        object_store_config = config["object_store"]
        signed_url_expiry = int(
            os.getenv("KP_OBJECT_STORE_SIGNED_URL_EXPIRY", object_store_config["signed_url_expiry"].split(":"[-1][-1]))
        )

        object_store = {
            "host": os.getenv("KP_OBJECT_STORE_HOST", object_store_config["host"].split(":"[-1][-1])),
            "port": os.getenv("KP_OBJECT_STORE_PORT", object_store_config["port"].split(":"[-1][-1])),
            "access_key": os.getenv("KP_OBJECT_STORE_ACCESS_KEY", object_store_config["access_key"].split(":"[-1][-1])),
            "secret_key": os.getenv("KP_OBJECT_STORE_SECRET_KEY", object_store_config["secret_key"].split(":"[-1][-1])),
            "signed_url_expiry": signed_url_expiry,
        }
        docker_services.wait_until_responsive(  # type: ignore
            timeout=60.0, pause=0.1, check=lambda: is_object_store_responsive(object_store)  # type: ignore
        )
    except Exception as e:
        pytest.fail(f"Failed to start minio container, error: {e}")


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


@pytest.fixture(scope="session")
def app_object_store(app_initialization_container: ApplicationContainer) -> MinIOObjectStore:
    return app_initialization_container.storage()


@pytest.fixture(scope="function")
def server(app_container: None) -> FastAPI:
    from lib.infrastructure.rest.main import create_app

    app = create_app()
    return app


@pytest.fixture(scope="function")
def httpx_client(server: FastAPI) -> TestClient:
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


def user_message() -> SQLAUserMessage:
    fake = Faker().unique

    message_contents = SQLAMessageContent(
        content=fake.text(max_nb_chars=70)[:-1] + "?",
        content_type=MessageContentTypeEnum.TEXT,
    )

    return SQLAUserMessage(
        id=int(str(fake.random_int(min=51, max=60)) + str(datetime.datetime.now().timestamp()).replace(".", "")[6:13]),
        message_contents=[message_contents],
        thread_id=1,
    )


@pytest.fixture(scope="function")
def fake_user_message() -> SQLAUserMessage:
    return user_message()


def agent_message() -> SQLAAgentMessage:
    fake = Faker().unique

    message_contents = SQLAMessageContent(
        content=fake.text(max_nb_chars=70)[:-1],
        content_type=MessageContentTypeEnum.TEXT,
    )

    return SQLAAgentMessage(
        id=int(str(fake.random_int(min=41, max=50)) + str(datetime.datetime.now().timestamp()).replace(".", "")[6:13]),
        message_contents=[message_contents],
        thread_id=1,
    )


@pytest.fixture(scope="function")
def fake_agent_message() -> SQLAAgentMessage:
    return agent_message()


def message_pair() -> Tuple[SQLAUserMessage, SQLAAgentMessage]:
    fake = Faker().unique

    user_message_contents = SQLAMessageContent(
        content=fake.text(max_nb_chars=70)[:-1] + "?",
        content_type=MessageContentTypeEnum.TEXT,
    )

    agent_message_contents = SQLAMessageContent(
        content=fake.text(max_nb_chars=70)[:-1],
        content_type=MessageContentTypeEnum.TEXT,
    )

    user_message = SQLAUserMessage(
        id=int(str(fake.random_int(min=21, max=30)) + str(datetime.datetime.now().timestamp()).replace(".", "")[6:13]),
        message_contents=[user_message_contents],
        thread_id=1,
    )
    agent_message = SQLAAgentMessage(
        id=int(str(fake.random_int(min=31, max=40)) + str(datetime.datetime.now().timestamp()).replace(".", "")[6:13]),
        message_contents=[agent_message_contents],
        thread_id=2,
    )

    return user_message, agent_message


@pytest.fixture(scope="function")
def fake_message_pair() -> Tuple[SQLAUserMessage, SQLAAgentMessage]:
    return message_pair()


TMessagePair = Tuple[SQLAUserMessage, SQLAAgentMessage]


def conversation(number_of_message_pairs: int = 1) -> SQLAConversation:
    """
    Creates a conversation with a title and a list of messages
    The messages are created by calling message_pair() number_of_message_pairs times, which will create a list alternating a SQLAUserMessage and a SQLAAgentMessage
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
    fake_description = fake.text(max_nb_chars=70)
    fake_external_id = uuid.uuid4()

    fake_conversations_init = tuple(
        conversation(random.randrange(1, up_bound_message_pairs_per_conversation + 1))
        for _ in range(number_of_conversations + 1)
    )
    fake_conversations = list(fake_conversations_init)

    return SQLAResearchContext(
        title=fake_title,
        description=fake_description,
        external_id=str(fake_external_id),
        conversations=fake_conversations,
    )


@pytest.fixture(scope="function")
def fake_research_context() -> SQLAResearchContext:
    return research_context()


def sqla_client() -> SQLAClient:
    fake = Faker().unique
    # Has to also be a valid minio bucket name
    fake_sub = f"{fake.name()}-{uuid.uuid4()}"

    return SQLAClient(
        sub=fake_sub,
    )


@pytest.fixture(scope="function")
def fake_client() -> SQLAClient:
    return sqla_client()


def client_with_conversation(number_of_research_contexts: int = 2) -> SQLAClient:
    client = sqla_client()

    fake_research_contexts_init = tuple(research_context() for _ in range(number_of_research_contexts + 1))
    fake_research_contexts = list(fake_research_contexts_init)
    #    fake_research_context = research_context()

    return SQLAClient(
        sub=client.sub,
        research_contexts=fake_research_contexts,
    )


@pytest.fixture(scope="function")
def fake_client_with_conversation() -> SQLAClient:
    return client_with_conversation()


def source_data() -> SQLASourceData:
    fake = Faker().unique

    # Validation is so good that now this fails, hardcode S3 for now
    # protocols = [
    # attr_name.__str__().lower() for attr_name in vars(ProtocolEnum) if not attr_name.__str__().startswith("_")
    # ]

    # protocol_choice: str = random.choice(protocols)
    # protocol = ProtocolEnum(protocol_choice)

    protocol = ProtocolEnum.S3

    statuses = [
        attr_name.__str__().lower()
        for attr_name in vars(SourceDataStatusEnum)
        if not attr_name.__str__().startswith("_")
    ]
    sd_status_choice: str = random.choice(statuses)
    sd_status = SourceDataStatusEnum(sd_status_choice)

    sd_name = fake.name()  # Name can be anything
    sd_relative_path = "".join(f"{uuid.uuid4()}-{fake.file_name()}".replace("-", "/").split())

    core_sd = SourceData(  # use the pydantic model to generate a proper one
        id=random.randint(1, 1000),
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        deleted=False,
        deleted_at=None,
        name=sd_name,
        relative_path=sd_relative_path,
        type="",  # type is generated automatically
        protocol=protocol,
        status=sd_status,
    )

    return SQLASourceData(
        name=core_sd.name,
        relative_path=core_sd.relative_path,
        type=core_sd.type,
        protocol=core_sd.protocol,
        status=core_sd.status,
    )


@pytest.fixture(scope="function")
def fake_source_data() -> SQLASourceData:
    return source_data()


@pytest.fixture(scope="function")
def fake_source_data_list() -> List[SQLASourceData]:
    return [source_data() for _ in range(10)]


def client_with_source_data(number_of_source_data: int = 3) -> SQLAClient:
    client = sqla_client()

    fake_source_data_init = tuple(source_data() for _ in range(number_of_source_data + 1))
    fake_source_data = list(fake_source_data_init)

    client.source_data.extend(fake_source_data)

    return client


@pytest.fixture(scope="function")
def fake_client_with_source_data() -> SQLAClient:
    return client_with_source_data()


@pytest.fixture(scope="function")
def fake_client_with_source_data_list() -> List[SQLAClient]:
    return [client_with_source_data() for _ in range(10)]


def client_with_research_context_and_sources(
    number_of_research_contexts: int = 2,
    number_of_new_source_data: int = 3,
) -> SQLAClient:
    client = sqla_client()

    fake_research_contexts_init = tuple(research_context() for _ in range(number_of_research_contexts + 1))
    fake_research_contexts = list(fake_research_contexts_init)

    fake_source_data_init = tuple(source_data() for _ in range(number_of_new_source_data + 1))
    fake_source_data = list(fake_source_data_init)

    # client.source_data.extend(fake_source_data)

    return SQLAClient(
        sub=client.sub,
        research_contexts=fake_research_contexts,
        source_data=fake_source_data,
    )


@pytest.fixture(scope="function")
def fake_client_with_research_context_and_sources() -> SQLAClient:
    return client_with_research_context_and_sources()


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


def llm() -> SQLALLM:
    fake = Faker().unique

    fake_name = f"{fake.name()}-{uuid.uuid4()}"

    return SQLALLM(
        llm_name=fake_name,
    )


@pytest.fixture(scope="function")
def fake_llm() -> SQLALLM:
    return llm()


@pytest.fixture(scope="function")
def test_file_path() -> str:
    test_content = b"test content: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

    with tempfile.NamedTemporaryFile(delete=False) as file:
        file.write(test_content)
        return file.name


@pytest.fixture(scope="function")
def test_output_dir_path() -> str:
    return tempfile.mkdtemp()
