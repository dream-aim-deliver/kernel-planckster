from typing import Any
from lib.core.ports.primary.list_source_data_for_research_context_primary_ports import (
    ListSourceDataForResearchContextInputPort,
    ListSourceDataForResearchContextOutputPort,
)
from lib.core.sdk.ioc_feature_container import BaseFeatureContainer

from dependency_injector import providers

from lib.core.usecase.list_source_data_for_research_context_usecase import ListSourceDataForResearchContextUseCase
from lib.infrastructure.controller.list_source_data_for_research_context_controller import (
    ListSourceDataForResearchContextController,
)
from lib.infrastructure.presenter.list_source_data_for_research_context_presenter import (
    ListSourceDataForResearchContextPresenter,
)


class ListSourceDataForResearchContextFeatureContainer(BaseFeatureContainer):
    research_context_repository: Any = providers.Dependency()

    presenter = providers.Factory[ListSourceDataForResearchContextOutputPort](ListSourceDataForResearchContextPresenter)

    usecase = providers.Factory[ListSourceDataForResearchContextInputPort](
        ListSourceDataForResearchContextUseCase, research_context_repository=research_context_repository
    )

    controller = providers.Factory(
        ListSourceDataForResearchContextController,
        usecase=usecase,
        presenter=presenter,
    )
