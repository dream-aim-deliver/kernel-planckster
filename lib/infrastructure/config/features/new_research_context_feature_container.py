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
    user_repository: Any = providers.Dependency()
    default_user_sid: Any = providers.Dependency()
    default_llm_name: Any = providers.Dependency()

    presenter = providers.Factory[NewResearchContextOutputPort](NewResearchContextPresenter)

    usecase = providers.Factory[NewResearchContextInputPort](NewResearchContextUseCase, user_repository=user_repository)

    controller = providers.Factory(
        NewResearchContextController,
        usecase=usecase,
        presenter=presenter,
        default_user_sid=default_user_sid,
        default_llm_name=default_llm_name,
    )
