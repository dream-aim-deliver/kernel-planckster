from typing import Any
from lib.core.ports.primary.list_conversations_primary_ports import (
    ListConversationsInputPort,
    ListConversationsOutputPort,
)
from lib.core.sdk.ioc_feature_container import BaseFeatureContainer
from lib.core.usecase.list_conversations_usecase import ListConversationsUseCase
from lib.infrastructure.controller.list_conversations_controller import ListConversationsController
from lib.infrastructure.presenter.list_conversations_presenter import ListConversationsPresenter

from dependency_injector import providers


class ListConversationsFeatureContainer(BaseFeatureContainer):
    research_context_repository: Any = providers.Dependency()
    presenter = providers.Factory[ListConversationsOutputPort](ListConversationsPresenter)

    usecase = providers.Factory[ListConversationsInputPort](
        ListConversationsUseCase, research_context_repository=research_context_repository
    )

    controller = providers.Factory(
        ListConversationsController,
        usecase=usecase,
        presenter=presenter,
    )
