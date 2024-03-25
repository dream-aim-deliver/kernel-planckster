from typing import Any
from lib.core.ports.primary.new_research_context_primary_ports import (
    NewResearchContextInputPort,
    NewResearchContextOutputPort,
)
from lib.core.sdk.ioc_feature_container import BaseFeatureContainer

from dependency_injector import providers
from lib.core.usecase.new_research_context_usecase import NewResearchContextUseCase
from lib.infrastructure.controller.new_research_context_controller import NewResearchContextController

from lib.infrastructure.presenter.new_research_context_presenter import NewResearchContextPresenter


class NewResearchContextFeatureContainer(BaseFeatureContainer):
    client_repository: Any = providers.Dependency()

    presenter = providers.Factory[NewResearchContextOutputPort](NewResearchContextPresenter)

    usecase = providers.Factory[NewResearchContextInputPort](
        NewResearchContextUseCase, client_repository=client_repository
    )

    controller = providers.Factory(
        NewResearchContextController,
        usecase=usecase,
        presenter=presenter,
    )
