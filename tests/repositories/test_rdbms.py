import docker

from lib.infrastructure.config.containers import ApplicationContainer
import pytest

from lib.infrastructure.repository.sqla.database import Database


def test_pg_container_is_available(app_raw_db: Database) -> None:
    client = docker.from_env()
    containers = client.containers.list()
    assert len(containers) != 0
    image_names = [container.image.tags[0] for container in containers]
    assert "postgres:latest" in image_names


def test_migrations_are_applied(app_container: ApplicationContainer) -> None:
    db = app_container.db()
    assert db is not None
    assert db.ping() is True
    assert db.engine is not None
