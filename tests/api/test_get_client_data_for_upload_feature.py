from datetime import datetime
import os
import random
import shutil
import requests
from lib.core.usecase.get_client_data_for_upload_usecase import GetClientDataForUploadUsecase
from lib.core.usecase_models.get_client_data_for_upload_usecase_models import (
    GetClientDataForUploadRequest,
    GetClientDataForUploadResponse,
)
from lib.core.view_model.get_client_data_for_upload_view_model import GetClientDataForUploadViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.get_client_data_for_upload_controller import (
    GetClientDataForUploadController,
    GetClientDataForUploadControllerParameters,
)
from lib.infrastructure.presenter.get_client_data_for_upload_presenter import GetClientDataForUploadPresenter
from lib.infrastructure.repository.minio.models import MinIOPFN
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLAClient


def test_get_client_data_for_upload_feature_usecase_presenter(
    app_container: ApplicationContainer,
    test_file_path: str,
    test_output_dir_path: str,
    fake_client_with_source_data: SQLAClient,
    db_session: TDatabaseFactory,
) -> None:
    presenter: GetClientDataForUploadPresenter = app_container.get_client_data_for_upload_feature.presenter()

    usecase: GetClientDataForUploadUsecase = app_container.get_client_data_for_upload_feature.usecase()

    assert usecase is not None

    file_path = test_file_path

    sqla_client = fake_client_with_source_data
    sqla_source_data = random.choice(sqla_client.source_data)

    with db_session() as session:
        session.add(sqla_client)
        session.commit()

        request = GetClientDataForUploadRequest(
            client_id=sqla_client.id,
            protocol=sqla_source_data.protocol,
            relative_path=sqla_source_data.relative_path,
        )
        response = usecase.execute(request=request)

        assert response is not None
        assert response.status == True
        assert isinstance(response, GetClientDataForUploadResponse)

        view_model = presenter.convert_response_to_view_model(response=response)

        assert view_model is not None
        assert view_model.status == True

        signed_url = view_model.signed_url

        assert signed_url

        # Now test that the signed_url actually works
        minio_repo = app_container.minio_file_repository()

        bucket_name = MinIOPFN.process_bucket_name(sqla_client.sub)

        pfn = minio_repo.store.protocol_and_relative_path_to_pfn(
            protocol=sqla_source_data.protocol,
            relative_path=sqla_source_data.relative_path,
            bucket_name=bucket_name,
        )
        minio_object = minio_repo.store.pfn_to_object_name(pfn)

        bucket_name = minio_object.bucket_name

        # Upload the file using the signed URL with a manual request
        with open(file_path, "rb") as file:
            res = requests.put(signed_url, data=file)
        assert res.status_code == 200

        # Check if the file is in the bucket
        objects = minio_repo.store.list_objects(bucket_name)
        assert minio_object in objects

        # Download file and test it's the same
        test_output_dir = test_output_dir_path
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        downloaded_file_path = f"{test_output_dir}/minio_downloaded_file-{timestamp}.txt"

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
        shutil.rmtree(test_output_dir)


def test_get_client_data_for_upload_feature_controller(
    app_container: ApplicationContainer,
    test_file_path: str,
    fake_client_with_source_data: SQLAClient,
    db_session: TDatabaseFactory,
) -> None:
    controller: GetClientDataForUploadController = app_container.get_client_data_for_upload_feature.controller()

    assert controller is not None
    assert isinstance(controller, GetClientDataForUploadController)

    sqla_client = fake_client_with_source_data
    sqla_source_data = random.choice(sqla_client.source_data)

    with db_session() as session:
        session.add(sqla_client)
        session.commit()

        controller_parameters = GetClientDataForUploadControllerParameters(
            client_id=sqla_client.id,
            protocol=sqla_source_data.protocol,
            relative_path=sqla_source_data.relative_path,
        )

        vm = controller.execute(parameters=controller_parameters)

        assert vm is not None
        assert isinstance(vm, GetClientDataForUploadViewModel)
        assert vm.status is True
        assert vm.signed_url

        os.remove(test_file_path)
