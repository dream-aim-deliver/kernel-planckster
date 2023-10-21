import docker

from lib.infrastructure.config.containers import Container
import pytest


@pytest.mark.usefixtures("with_rdbms")
def test_pg_container_is_available() -> None:
    client = docker.from_env()
    containers = client.containers.list()
    assert len(containers) != 0
    image_names = [container.image.tags[0] for container in containers]
    assert "postgres:latest" in image_names


@pytest.mark.usefixtures("with_rdbms_migrations")
def test_migrations_are_applied(app_container: Container) -> None:
    db = app_container.db()
    assert db is not None
    assert db.ping() is True
    assert db.engine is not None
