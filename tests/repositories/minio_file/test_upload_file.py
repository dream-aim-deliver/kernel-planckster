from datetime import datetime
import os
import random
import shutil
import requests

from lib.core.entity.models import ProtocolEnum
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.minio.models import MinIOPFN
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLAClient, SQLASourceData
from lib.infrastructure.repository.sqla.utils import convert_sqla_client_to_core_client


def test_obtain_working_signed_url_to_get_client_data_for_upload(
    app_initialization_container: ApplicationContainer,
    test_file_path: str,
    test_output_dir_path: str,
    fake_client: SQLAClient,
    fake_source_data: SQLASourceData,
    db_session: TDatabaseFactory,
) -> None:
    minio_repo = app_initialization_container.minio_file_repository()

    sqla_client = fake_client
    source_data = fake_source_data
    sqla_client.source_data.extend([source_data])

    file_path = test_file_path

    with db_session() as session:
        session.add(sqla_client)
        session.commit()

        sqla_client = source_data.client
        core_client = convert_sqla_client_to_core_client(sqla_client)

        dto = minio_repo.get_client_data_for_upload(
            client=core_client,
            protocol=source_data.protocol,
            relative_path=source_data.relative_path,  # NOTE: Not the same as the local file path
        )

        assert dto.status == True
        assert dto.credentials

        signed_url = dto.credentials

        bucket_name = MinIOPFN.process_bucket_name(core_client.sub)

        pfn = minio_repo.store.protocol_and_relative_path_to_pfn(
            protocol=source_data.protocol,
            relative_path=source_data.relative_path,
            bucket_name=bucket_name,
        )

        minio_object = minio_repo.store.pfn_to_object_name(pfn)

        # Upload the file using the signed URL with a manual request
        with open(file_path, "rb") as file:
            res = requests.put(signed_url, data=file)

        assert res.status_code == 200

        # Check if the file is in the bucket
        objects = minio_repo.store.list_objects(minio_object.bucket_name)
        assert minio_object in objects

        # Download file and test it's the same
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        downloaded_file_path = f"{test_output_dir_path}/minio_downloaded_file-{timestamp}.txt"

        # create folder if it doesn't exist
        os.makedirs(os.path.dirname(downloaded_file_path), exist_ok=True)

        minio_repo.store.client.fget_object(minio_object.bucket_name, minio_object.object_name, downloaded_file_path)

        assert os.path.exists(downloaded_file_path)

        with open(downloaded_file_path, "rb") as file:
            downloaded_content = file.read()

        with open(file_path, "rb") as file:
            original_content = file.read()

        assert downloaded_content == original_content

        os.remove(file_path)
        os.remove(downloaded_file_path)
        shutil.rmtree(test_output_dir_path)


def test_error_obtain_signed_url_to_get_client_data_for_upload_either_input_is_none(
    app_initialization_container: ApplicationContainer,
    fake_client: SQLAClient,
) -> None:
    minio_repo = app_initialization_container.minio_file_repository()

    dto = minio_repo.get_client_data_for_upload(
        client=None,  # type: ignore
        protocol=random.choice([p for p in ProtocolEnum]),
        relative_path="some_relative_path",
    )

    assert dto.status == False
    assert dto.errorCode == -1
    assert dto.errorType == "ClientNotProvided"
    assert dto.data == None

    dto = minio_repo.get_client_data_for_upload(
        client=fake_client, protocol=None, relative_path="some_relative_path"  # type: ignore
    )

    assert dto.status == False
    assert dto.errorCode == -1
    assert dto.errorType == "ProtocolNotProvided"
    assert dto.data == None

    dto = minio_repo.get_client_data_for_upload(
        client=fake_client, protocol=random.choice([p for p in ProtocolEnum]), relative_path=None  # type: ignore
    )

    assert dto.status == False
    assert dto.errorCode == -1
    assert dto.errorType == "RelativePathNotProvided"
    assert dto.data == None
