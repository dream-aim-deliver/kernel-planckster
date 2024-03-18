import docker

from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.minio.object_store import ObjectStore


def test_minio_container_is_available(app_object_store: ObjectStore) -> None:
    client = docker.from_env()
    containers = client.containers.list()
    assert len(containers) != 0
    image_names = [container.image.tags[0] for container in containers]
    assert "quay.io/minio/minio:latest" in image_names


def test_minio_bucket_is_created(app_container: ApplicationContainer) -> None:
    storage = app_container.storage()
    assert storage is not None
    assert storage.ping() is True
    assert storage.bucket_exists(storage.bucket) is True
