from datetime import datetime
import os
import requests
from lib.core.usecase.upload_file_usecase import UploadFileUsecase
from lib.core.usecase_models.upload_file_usecase_models import UploadFileRequest, UploadFileResponse
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.upload_file_controller import UploadFileControllerParameters
from lib.infrastructure.presenter.upload_file_presenter import UploadFilePresenter


def test_upload_file_feature_usecase_presenter(
    app_container: ApplicationContainer,
    test_file_path: str,
    test_dir_path: str,
) -> None:
    presenter: UploadFilePresenter = app_container.upload_file_feature.presenter()

    usecase: UploadFileUsecase = app_container.upload_file_feature.usecase()

    assert usecase is not None

    file_path = test_file_path

    request = UploadFileRequest(file_path=file_path)
    response = usecase.execute(request=request)

    assert response is not None
    assert response.status == True
    assert isinstance(response, UploadFileResponse)

    view_model = presenter.convert_response_to_view_model(response=response)

    assert view_model is not None
    assert view_model.status == True

    lfn, signed_url = view_model.lfn, view_model.signed_url

    assert lfn
    assert signed_url

    # Now test that the signed_url actually works
    minio_repo = app_container.minio_file_repository()

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
    test_output_dir_path = test_dir_path
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


def test_upload_file_feature_controller(
    app_container: ApplicationContainer,
    test_file_path: str,
) -> None:
    controller = app_container.upload_file_feature.controller()

    assert controller is not None

    file_path = test_file_path
    controller_parameters = UploadFileControllerParameters(
        file_path=file_path,
    )

    vm = controller.execute(parameters=controller_parameters)
    assert vm is not None
    assert vm.status is True
    assert vm.lfn
    assert vm.signed_url
