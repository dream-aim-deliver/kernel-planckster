import os

import requests
from lib.core.usecase.get_client_data_for_download_usecase import GetClientDataForDownloadUseCase
from lib.core.usecase_models.get_client_data_for_download_usecase_models import (
    GetClientDataForDownloadRequest,
    GetClientDataForDownloadResponse,
)
from lib.core.view_model.get_client_data_for_download_view_model import GetClientDataForDownloadViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.presenter.get_client_data_for_download_presenter import GetClientDataForDownloadPresenter
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLAKnowledgeSource, SQLASourceData
from lib.infrastructure.repository.sqla.utils import convert_core_lfn_to_sqla_lfn


def test_get_client_data_for_download_feature(
    app_container: ApplicationContainer,
    test_file_path: str,
    fake_knowledge_source_with_source_data: SQLAKnowledgeSource,
    db_session: TDatabaseFactory,
) -> None:
    presenter: GetClientDataForDownloadPresenter = app_container.get_client_data_for_download_feature.presenter()
    usecase: GetClientDataForDownloadUseCase = app_container.get_client_data_for_download_feature.usecase()

    assert presenter is not None
    assert usecase is not None

    file_path = test_file_path

    fp_to_lfn_dto = app_container.minio_file_repository().file_path_to_lfn(file_path=file_path)

    assert fp_to_lfn_dto.status
    assert fp_to_lfn_dto.lfn

    # Manually upload file
    minio_file_repo = app_container.minio_file_repository()
    minio_store = minio_file_repo.store

    lfn = fp_to_lfn_dto.lfn
    pfn = minio_store.lfn_to_pfn(lfn)
    object_name = minio_store.pfn_to_object_name(pfn)

    minio_store.client.fput_object(bucket_name=minio_store.bucket, object_name=object_name, file_path=file_path)

    # Manually create the LFN in the database within a Source Data
    ks = fake_knowledge_source_with_source_data
    source_data_base = ks.source_data[0]

    sqla_lfn = convert_core_lfn_to_sqla_lfn(lfn)

    source_data = SQLASourceData(
        name=source_data_base.name,
        type=source_data_base.type,
        lfn=sqla_lfn,
        status=source_data_base.status,
    )

    ks.source_data.append(source_data)

    with db_session() as session:
        session.add(ks)
        session.commit()

    # Now ask for the download information using the usecase
    lfn_str = lfn.to_json()
    request = GetClientDataForDownloadRequest(lfn_str=lfn_str)
    response = usecase.execute(request=request)

    assert response is not None
    assert response.status == True
    assert isinstance(response, GetClientDataForDownloadResponse)

    view_model = presenter.convert_response_to_view_model(response=response)

    assert view_model is not None
    assert view_model.status == True
    assert isinstance(view_model, GetClientDataForDownloadViewModel)

    assert view_model.lfn == lfn
    assert view_model.signed_url

    signed_url = view_model.signed_url

    # Now test that the signed_url actually works
    out_file_path = f"{file_path}.downloaded"

    try:
        download_res = requests.get(signed_url)
        with open(out_file_path, "wb") as f:
            f.write(download_res.content)

        # Read both files and assert they're the same
        with open(file_path, "rb") as f:
            original_content = f.read()

        with open(out_file_path, "rb") as f:
            downloaded_content = f.read()

        assert original_content == downloaded_content

    finally:
        # Clean up
        os.remove(out_file_path)
        os.remove(file_path)
