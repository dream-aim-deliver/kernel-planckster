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
    presenter = providers.Factory[ListConversationsOutputPort](ListConversationsPresenter)

    usecase = providers.Factory[ListConversationsInputPort](
        ListConversationsUseCase,
    )

    controller = providers.Factory(
        ListConversationsController,
        usecase=usecase,
        presenter=presenter,
    )
