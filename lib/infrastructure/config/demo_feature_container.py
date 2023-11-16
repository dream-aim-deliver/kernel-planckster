from dependency_injector import containers, providers

from lib.core.ports.primary.demo_ports import DemoInputPort, DemoOutputPort
from lib.core.sdk.feature import BaseFeatureDescriptor
from lib.core.usecase.demo_usecase import DemoUseCase
from lib.infrastructure.controller.demo_controller import DemoController
from lib.infrastructure.presenter.demo_presenter import DemoPresenter


class DemoFeatureContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    presenter = providers.Factory[DemoOutputPort](
        DemoPresenter,
    )

    usecase = providers.Factory[DemoInputPort](
        DemoUseCase,
    )

    controller = providers.Factory(
        DemoController,
        usecase=usecase,
        presenter=presenter,
    )

    feature_descriptor = providers.Factory(
        BaseFeatureDescriptor,
        name=config.name,
        description=config.description,
        version=config.version,
        verb=config.verb,
        endpoint=config.endpoint,
        enabled=config.enabled,
        auth=config.auth,
    )
