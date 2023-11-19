from typing import Any
from lib.core.ports.primary.new_source_data_primary_ports import NewSourceDataInputPort, NewSourceDataOutputPort
from lib.core.sdk.ioc_feature_container import BaseFeatureContainer

from dependency_injector import providers
from lib.core.usecase.new_source_data_usecase import NewSourceDataUseCase
from lib.infrastructure.controller.new_source_data_controller import NewSourceDataController

from lib.infrastructure.presenter.new_source_data_presenter import NewSourceDataPresenter


class NewSourceDataFeatureContainer(BaseFeatureContainer):
    knowledge_source_repository: Any = providers.Dependency()

    presenter = providers.Factory[NewSourceDataOutputPort](NewSourceDataPresenter)

    usecase = providers.Factory[NewSourceDataInputPort](
        NewSourceDataUseCase, knowledge_source_repository=knowledge_source_repository
    )

    controller = providers.Factory(
        NewSourceDataController,
        usecase=usecase,
        presenter=presenter,
    )
