from typing import Any
from lib.core.ports.primary.upload_file_primary_ports import UploadFileInputPort, UploadFileOutputPort
from lib.core.sdk.ioc_feature_container import BaseFeatureContainer

from dependency_injector import providers

from lib.core.usecase.upload_file_usecase import UploadFileUsecase
from lib.infrastructure.controller.upload_file_controller import UploadFileController
from lib.infrastructure.presenter.upload_file_presenter import UploadFilePresenter


class UploadFileFeatureContainer(BaseFeatureContainer):
    file_repository: Any = providers.Dependency()

    presenter = providers.Factory[UploadFileOutputPort](UploadFilePresenter)

    usecase = providers.Factory[UploadFileInputPort](UploadFileUsecase, file_repository=file_repository)

    controller = providers.Factory(
        UploadFileController,
        usecase=usecase,
        presenter=presenter,
    )
