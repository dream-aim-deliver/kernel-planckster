from contextlib import _GeneratorContextManager
import datetime
import os
import random
from typing import Annotated, Any, Callable, Generator, Generic, List, Tuple, TypeVar
from faker import Faker
from faker.proxy import UniqueProxy
import pytest
from tomlkit import date
import lib
from lib.core.entity.models import Citation
from lib.infrastructure.config.containers import Container
from alembic.config import Config
from alembic import command
from sqlalchemy.orm import Session

from lib.infrastructure.repository.sqla.database import Database, TDatabaseFactory
from lib.infrastructure.repository.sqla.models import (
    ModelBase,
    SQLACitation,
    SQLAConversation,
    SQLAKnowledgeSource,
    SQLAMessageBase,
    SQLAMessageQuery,
    SQLAMessageResponse,
    SQLAResearchContext,
    SQLAUser,
)


container = Container()
print(container.config())
container.wire(modules=[lib])


# set autouse=True to automatically inject the container into all tests
@pytest.fixture(scope="session")
def app_container() -> Container:
    return container


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig: Annotated[pytest.Config, pytest.fixture]) -> str:
    return os.path.join(str(pytestconfig.rootdir), "tests", "docker-compose.yml")  # type: ignore


# set autouse=True to automatically inject the postgres into all tests
@pytest.fixture(scope="session")
def with_rdbms(
    app_container: Container,
    docker_services: pytest.fixture,  # type: ignore
) -> Database:
    """Ensure that a postgres container is running before running tests"""

    def is_responsive() -> bool:
        try:
            db = app_container.db()
            return db.ping()
        except Exception as e:
            return False

    try:
        docker_services.wait_until_responsive(timeout=60.0, pause=0.1, check=lambda: is_responsive())  # type: ignore
    except Exception as e:
        pytest.fail(f"Failed to start postgres container, error: {e}")

    return app_container.db()


@pytest.fixture(scope="session")
def with_rdbms_migrations(request: pytest.FixtureRequest, with_rdbms: Database) -> None:
    """Run alembic migrations before running tests and tear them down after"""
    alembic_ini_path = os.path.join(str(request.config.rootdir), "alembic.ini")  # type: ignore
    alembic_cfg = Config(alembic_ini_path)

    alembic_scripts_path = os.path.join(str(request.config.rootdir), "alembic")  # type: ignore
    alembic_cfg.set_main_option("script_location", alembic_scripts_path)

    alembic_cfg.set_main_option("sqlalchemy.url", container.db().url)

    try:
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        pytest.fail("Failed to run migrations, error: {e}")
    # request.addfinalizer(lambda: command.downgrade(alembic_cfg, "base"))


@pytest.fixture(scope="function")
def db_session(with_rdbms_migrations: None) -> Generator[Callable[[], _GeneratorContextManager[Session]], None, None]:
    """Create a new database session for each test"""
    yield container.db().session


@pytest.fixture(scope="function")
def fake() -> UniqueProxy:
    return Faker().unique


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

    dt2 = fake.date_time_between_dates(
        datetime_start=dt1, datetime_end=datetime.datetime.now() - datetime.timedelta(weeks=1)
    )

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


def conversation(number_of_message_pairs: int = 2) -> SQLAConversation:
    """
    Creates a conversation with a title and a list of messages
    The messages are created by calling message_pair() number_of_message_pairs times, which will create a list alternating a SQLAMessageQuery and a SQLAMessageResponse
    """
    fake = Faker().unique

    fake_title = fake.text(max_nb_chars=70)

    nested_tup = tuple(message_pair() for _ in range(number_of_message_pairs))
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
    number_of_conversations: int = 4, up_bound_message_pairs_per_conversation: int = 5
) -> SQLAResearchContext:
    """
    Creates a research context with a title and a list of conversations
    The conversations are created by calling conversation() number_of_conversations times, with an upper bound of maximum possible message pairs per conversation of up_bound_messages_per_conversation
    """
    fake = Faker().unique

    fake_title = fake.name()

    fake_conversations_init = tuple(
        conversation(random.randrange(1, up_bound_message_pairs_per_conversation))
        for _ in range(number_of_conversations)
    )
    fake_conversations = list(fake_conversations_init)

    return SQLAResearchContext(
        title=fake_title,
        conversations=fake_conversations,
    )


@pytest.fixture(scope="function")
def fake_research_context() -> SQLAResearchContext:
    return research_context()


def user_with_conversation(number_of_research_contexts: int = 2) -> SQLAUser:
    fake = Faker().unique

    fake_sid = fake.name()

    fake_research_contexts_init = tuple(research_context() for _ in range(number_of_research_contexts))
    fake_research_contexts = list(fake_research_contexts_init)
    #    fake_research_context = research_context()

    return SQLAUser(
        sid=fake_sid,
        research_contexts=fake_research_contexts,
    )


@pytest.fixture(scope="function")
def fake_user_with_conversation() -> SQLAUser:
    return user_with_conversation()
