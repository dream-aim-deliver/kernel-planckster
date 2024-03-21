from datetime import datetime
import os
import shutil
import requests
from lib.core.usecase.get_client_data_for_upload_usecase import GetClientDataForUploadUsecase
from lib.core.usecase_models.get_client_data_for_upload_usecase_models import (
    GetClientDataForUploadRequest,
    GetClientDataForUploadResponse,
)
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.get_client_data_for_upload_controller import (
    GetClientDataForUploadControllerParameters,
)
from lib.infrastructure.presenter.get_client_data_for_upload_presenter import GetClientDataForUploadPresenter


def test_get_client_data_for_upload_feature_usecase_presenter(
    app_container: ApplicationContainer,
    test_file_path: str,
    test_output_dir_path: str,
) -> None:
    presenter: GetClientDataForUploadPresenter = app_container.get_client_data_for_upload_feature.presenter()

    usecase: GetClientDataForUploadUsecase = app_container.get_client_data_for_upload_feature.usecase()

    minio_file_repo = app_container.minio_file_repository()

    assert usecase is not None

    file_path = test_file_path
    fp_to_lfn_dto = minio_file_repo.file_path_to_lfn(file_path=file_path)

    assert fp_to_lfn_dto.status
    assert fp_to_lfn_dto.lfn

    lfn_str = fp_to_lfn_dto.lfn.to_json()

    request = GetClientDataForUploadRequest(lfn_str=lfn_str)
    response = usecase.execute(request=request)

    assert response is not None
    assert response.status == True
    assert isinstance(response, GetClientDataForUploadResponse)

    view_model = presenter.convert_response_to_view_model(response=response)

    assert view_model is not None
    assert view_model.status == True

    dto_lfn, signed_url = view_model.lfn, view_model.signed_url

    assert dto_lfn
    assert signed_url

    # Now test that the signed_url actually works
    minio_repo = app_container.minio_file_repository()

    pfn = minio_repo.store.lfn_to_pfn(dto_lfn)
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
    test_output_dir_path = test_output_dir_path
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

    os.remove(test_file_path)
    os.remove(downloaded_file_path)
    shutil.rmtree(test_output_dir_path)


def test_get_client_data_for_upload_feature_controller(
    app_container: ApplicationContainer,
    test_file_path: str,
) -> None:
    controller = app_container.get_client_data_for_upload_feature.controller()

    assert controller is not None

    file_path = test_file_path

    minio_file_repo = app_container.minio_file_repository()
    fp_to_lfn_dto = minio_file_repo.file_path_to_lfn(file_path=file_path)

    assert fp_to_lfn_dto.status
    assert fp_to_lfn_dto.lfn

    lfn_str = fp_to_lfn_dto.lfn.to_json()

    controller_parameters = GetClientDataForUploadControllerParameters(
        lfn_str=lfn_str,
    )

    vm = controller.execute(parameters=controller_parameters)
    assert vm is not None
    assert vm.status is True
    assert vm.lfn
    assert vm.signed_url

    os.remove(test_file_path)
