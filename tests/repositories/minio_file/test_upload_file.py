from datetime import datetime
import os
import requests

from lib.infrastructure.config.containers import ApplicationContainer


def test_obtain_working_signed_url_to_upload_file(
    app_initialization_container: ApplicationContainer,
    test_file_path: str,
    test_output_dir_path: str,
) -> None:
    minio_repo = app_initialization_container.minio_file_repository()

    file_path = test_file_path
    lfn = minio_repo.file_path_to_lfn(file_path=file_path).lfn
    assert lfn

    dto = minio_repo.upload_file(lfn=lfn)

    assert dto.status == True
    assert dto.lfn
    assert dto.auth

    lfn, signed_url = dto.lfn, dto.auth

    pfn = minio_repo.store.lfn_to_pfn(lfn)
    object_name = minio_repo.store.pfn_to_object_name(pfn)

    bucket_name = minio_repo.store.bucket

    # Upload the file using the signed URL with a manual request
    with open(file_path, "rb") as file:
        res = requests.put(signed_url, data=file)

    assert res.status_code == 200

    # Check if the file is in the bucket

    objects = minio_repo.store.list_objects(bucket_name)
    assert object_name in objects

    # Download file and test it's the same
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    downloaded_file_path = f"{test_output_dir_path}/minio_downloaded_file-{timestamp}.txt"

    # create folder if it doesn't exist
    os.makedirs(os.path.dirname(downloaded_file_path), exist_ok=True)

    minio_repo.store.client.fget_object(bucket_name, object_name, downloaded_file_path)

    assert os.path.exists(downloaded_file_path)

    with open(downloaded_file_path, "rb") as file:
        downloaded_content = file.read()

    with open(file_path, "rb") as file:
        original_content = file.read()

    assert downloaded_content == original_content

    os.remove(downloaded_file_path)


def test_error_obtain_signed_url_to_upload_file_none_lfn(
    app_initialization_container: ApplicationContainer,
) -> None:
    minio_repo = app_initialization_container.minio_file_repository()

    dto = minio_repo.upload_file(lfn=None)  # type: ignore

    assert dto.status == False
    assert dto.errorCode == -1
    assert dto.errorMessage == "LFN cannot be None"
    assert dto.errorName == "LFNNotProvided"
    assert dto.errorType == "LFNNotProvided"
    assert dto.data == None
