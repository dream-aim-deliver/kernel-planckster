from dependency_injector import containers, providers

from lib.core.ports.primary.demo_ports import DemoInputPort, DemoOutputPort
from lib.core.sdk.feature_descriptor import BaseFeatureDescriptor
from lib.core.sdk.ioc_feature_container import BaseFeatureContainer
from lib.core.usecase.demo_usecase import DemoUseCase
from lib.infrastructure.controller.demo_controller import DemoController
from lib.infrastructure.presenter.demo_presenter import DemoPresenter


class DemoFeatureContainer(BaseFeatureContainer):
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
