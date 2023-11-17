from faker import Faker
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory


def test_get_research_context(app_container: ApplicationContainer, db_session: TDatabaseFactory, faker: Faker) -> None:
    pass
