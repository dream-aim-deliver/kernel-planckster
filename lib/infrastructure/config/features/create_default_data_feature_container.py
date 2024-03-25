from typing import Any
from lib.core.ports.primary.create_default_data_primary_ports import (
    CreateDefaultDataInputPort,
    CreateDefaultDataOutputPort,
)
from lib.core.sdk.ioc_feature_container import BaseFeatureContainer

from dependency_injector import providers
from lib.core.usecase.create_default_data_usecase import CreateDefaultDataUseCase
from lib.infrastructure.controller.create_default_data_controller import CreateDefaultDataController

from lib.infrastructure.presenter.create_default_data_presenter import CreateDefaultDataPresenter


class CreateDefaultDataFeatureContainer(BaseFeatureContainer):
    session_factory: Any = providers.Dependency()
    default_client_sub: Any = providers.Dependency()
    default_llm_name: Any = providers.Dependency()

    presenter = providers.Factory[CreateDefaultDataOutputPort](
        CreateDefaultDataPresenter,
    )

    usecase = providers.Factory[CreateDefaultDataInputPort](CreateDefaultDataUseCase, session_factory=session_factory)

    controller = providers.Factory(
        CreateDefaultDataController,
        usecase=usecase,
        presenter=presenter,
        default_client_sub=default_client_sub,
        default_llm_name=default_llm_name,
    )
