from datetime import datetime
import os
import shutil
import requests
from lib.infrastructure.config.containers import ApplicationContainer


def test_obtain_working_signed_url_to_get_client_data_for_download(
    app_initialization_container: ApplicationContainer,
    test_file_path: str,
    test_output_dir_path: str,
) -> None:
    minio_repo = app_initialization_container.minio_file_repository()

    file_path = test_file_path
    lfn = minio_repo.file_path_to_lfn(file_path).lfn
    assert lfn

    pfn = minio_repo.store.lfn_to_pfn(lfn)
    object_name = minio_repo.store.pfn_to_object_name(pfn)
    bucket_name = minio_repo.store.bucket

    minio_repo.store.client.fput_object(bucket_name, object_name, file_path)

    dto = minio_repo.get_client_data_for_download(lfn)

    assert dto.status == True
    assert dto.lfn
    assert dto.credentials

    lfn_from_dto, signed_url = dto.lfn, dto.credentials

    assert lfn_from_dto == lfn

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

    lfn = None

    dto = minio_repo.get_client_data_for_download(lfn)  # type: ignore

    assert dto.status == False
    assert dto.lfn == None
    assert dto.credentials == None
    assert dto.errorCode == -1
    assert dto.errorMessage == "LFN cannot be None"
    assert dto.errorName == "LFNNotProvided"
    assert dto.errorType == "LFNNotProvided"
