from typing import Any
from lib.core.ports.primary.list_source_data_primary_ports import ListSourceDataInputPort, ListSourceDataOutputPort
from lib.core.sdk.ioc_feature_container import BaseFeatureContainer

from dependency_injector import providers
from lib.core.usecase.list_source_data_usecase import ListSourceDataUseCase
from lib.infrastructure.controller.list_source_data_controller import ListSourceDataController

from lib.infrastructure.presenter.list_source_data_presenter import ListSourceDataPresenter


class ListSourceDataFeatureContainer(BaseFeatureContainer):
    source_data_repository: Any = providers.Dependency()

    presenter = providers.Factory[ListSourceDataOutputPort](ListSourceDataPresenter)

    usecase = providers.Factory[ListSourceDataInputPort](
        ListSourceDataUseCase, source_data_repository=source_data_repository
    )

    controller = providers.Factory(
        ListSourceDataController,
        usecase=usecase,
        presenter=presenter,
    )
