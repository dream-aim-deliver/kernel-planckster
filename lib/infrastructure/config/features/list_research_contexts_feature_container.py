from typing import Any
from lib.core.ports.primary.list_research_contexts_primary_ports import (
    ListResearchContextsInputPort,
    ListResearchContextsOutputPort,
)
from lib.core.sdk.ioc_feature_container import BaseFeatureContainer


from dependency_injector import providers
from lib.core.usecase.list_research_contexts_usecase import ListResearchContextsUseCase
from lib.infrastructure.controller.list_research_contexts_controller import ListResearchContextsController

from lib.infrastructure.presenter.list_research_contexts_presenter import ListResearchContextsPresenter


class ListResearchContextsFeatureContainer(BaseFeatureContainer):
    client_repository: Any = providers.Dependency()
    presenter = providers.Factory[ListResearchContextsOutputPort](ListResearchContextsPresenter)

    usecase = providers.Factory[ListResearchContextsInputPort](
        ListResearchContextsUseCase, client_repository=client_repository
    )

    controller = providers.Factory(
        ListResearchContextsController,
        usecase=usecase,
        presenter=presenter,
    )
