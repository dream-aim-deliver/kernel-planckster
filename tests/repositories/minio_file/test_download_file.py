from datetime import datetime
import os
import shutil
import requests
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.minio.models import MinIOPFN
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLAClient, SQLASourceData
from lib.infrastructure.repository.sqla.utils import (
    convert_sqla_client_to_core_client,
    convert_sqla_source_data_to_core_source_data,
)


def test_obtain_working_signed_url_to_get_client_data_for_download(
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
    source_data.client = sqla_client

    file_path = test_file_path

    with db_session() as session:
        session.add(source_data)
        session.commit()

        sqla_client = source_data.client
        core_client = convert_sqla_client_to_core_client(sqla_client)
        core_source_data = convert_sqla_source_data_to_core_source_data(source_data)

        bucket_name = MinIOPFN.process_bucket_name(core_client.sub)

        pfn = minio_repo.store.protocol_and_relative_path_to_pfn(
            protocol=source_data.protocol,
            relative_path=source_data.relative_path,
            bucket_name=bucket_name,
        )

        minio_object = minio_repo.store.pfn_to_object_name(pfn)

        minio_repo.store.create_bucket_if_not_exists(minio_object.bucket_name)
        minio_repo.store.client.fput_object(minio_object.bucket_name, minio_object.object_name, file_path)

        dto = minio_repo.get_client_data_for_download(
            client=core_client,
            source_data=core_source_data,
        )

        assert dto.status == True
        assert dto.credentials

        signed_url = dto.credentials

        # Download the file using the signed URL with a manual request
        res = requests.get(signed_url)
        assert res.status_code == 200

        # Check if the file is the same
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        downloaded_file_path = f"{test_output_dir_path}/minio_downloaded_file-{timestamp}.txt"

        # create folder if it doesn't exist
        os.makedirs(os.path.dirname(downloaded_file_path), exist_ok=True)

        with open(downloaded_file_path, "wb") as file:
            file.write(res.content)

        assert os.path.exists(downloaded_file_path)

        with open(downloaded_file_path, "rb") as file:
            downloaded_content = file.read()

        with open(file_path, "rb") as file:
            original_content = file.read()

        assert downloaded_content == original_content

        # Clean up
        os.remove(test_file_path)
        os.remove(downloaded_file_path)
        shutil.rmtree(test_output_dir_path)


def test_obtain_working_signed_url_to_get_client_data_for_download_with_none_lfn(
    app_initialization_container: ApplicationContainer,
) -> None:
    minio_repo = app_initialization_container.minio_file_repository()

    dto = minio_repo.get_client_data_for_download(
        client=None,  # type: ignore
        source_data=None,  # type: ignore
    )

    assert dto.status == False
    assert dto.credentials == None
    assert dto.errorCode == -1
