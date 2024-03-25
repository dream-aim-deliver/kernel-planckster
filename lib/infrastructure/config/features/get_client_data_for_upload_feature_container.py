from typing import Any
from lib.core.ports.primary.get_client_data_for_upload_primary_ports import (
    GetClientDataForUploadInputPort,
    GetClientDataForUploadOutputPort,
)
from lib.core.sdk.ioc_feature_container import BaseFeatureContainer

from dependency_injector import providers

from lib.core.usecase.get_client_data_for_upload_usecase import GetClientDataForUploadUsecase
from lib.infrastructure.controller.get_client_data_for_upload_controller import GetClientDataForUploadController
from lib.infrastructure.presenter.get_client_data_for_upload_presenter import GetClientDataForUploadPresenter


class GetClientDataForUploadFeatureContainer(BaseFeatureContainer):
    client_repository: Any = providers.Dependency()
    file_repository: Any = providers.Dependency()

    presenter = providers.Factory[GetClientDataForUploadOutputPort](GetClientDataForUploadPresenter)

    usecase = providers.Factory[GetClientDataForUploadInputPort](
        GetClientDataForUploadUsecase, client_repository=client_repository, file_repository=file_repository
    )

    controller = providers.Factory(
        GetClientDataForUploadController,
        usecase=usecase,
        presenter=presenter,
    )
