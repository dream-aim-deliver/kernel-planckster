from typing import Any
from lib.core.ports.primary.extend_research_context_primary_ports import (
    ExtendResearchContextInputPort,
    ExtendResearchContextOutputPort,
)
from lib.core.sdk.ioc_feature_container import BaseFeatureContainer

from dependency_injector import providers

from lib.core.usecase.extend_research_context_usecase import ExtendResearchContextUseCase

from lib.infrastructure.controller.extend_research_context_controller import ExtendResearchContextController
from lib.infrastructure.presenter.extend_research_context_presenter import ExtendResearchContextPresenter


class ExtendResearchContextFeatureContainer(BaseFeatureContainer):
    client_repository: Any = providers.Dependency()
    research_context_repository: Any = providers.Dependency()

    presenter = providers.Factory[ExtendResearchContextOutputPort](ExtendResearchContextPresenter)

    usecase = providers.Factory[ExtendResearchContextInputPort](
        ExtendResearchContextUseCase,
        client_repository=client_repository,
        research_context_repository=research_context_repository,
    )

    controller = providers.Factory(
        ExtendResearchContextController,
        usecase=usecase,
        presenter=presenter,
    )
