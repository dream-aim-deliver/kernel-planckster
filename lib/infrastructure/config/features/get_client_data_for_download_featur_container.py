from typing import Any
from dependency_injector import providers

from lib.core.ports.primary.get_client_data_for_download_primary_ports import (
    GetClientDataForDownloadInputPort,
    GetClientDataForDownloadOutputPort,
)
from lib.core.sdk.ioc_feature_container import BaseFeatureContainer
from lib.core.usecase.get_client_data_for_download_usecase import GetClientDataForDownloadUseCase
from lib.infrastructure.controller.get_client_data_for_download_controller import GetClientDataForDownloadController
from lib.infrastructure.presenter.get_client_data_for_download_presenter import GetClientDataForDownloadPresenter


class GetClientDataForDownloadFeatureContainer(BaseFeatureContainer):
    file_repository: Any = providers.Dependency()
    source_data_repository: Any = providers.Dependency()

    presenter = providers.Factory[GetClientDataForDownloadOutputPort](GetClientDataForDownloadPresenter)

    usecase = providers.Factory[GetClientDataForDownloadInputPort](
        GetClientDataForDownloadUseCase, file_repository=file_repository, source_data_repository=source_data_repository
    )

    controller = providers.Factory(
        GetClientDataForDownloadController,
        usecase=usecase,
        presenter=presenter,
    )
