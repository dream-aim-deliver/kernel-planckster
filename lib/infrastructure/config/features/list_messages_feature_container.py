from typing import Any
from dependency_injector import providers

from lib.core.ports.primary.list_messages_primary_ports import ListMessagesInputPort, ListMessagesOutputPort
from lib.core.sdk.ioc_feature_container import BaseFeatureContainer
from lib.core.usecase.list_messages_usecase import ListMessagesUseCase
from lib.infrastructure.controller.list_messages_controller import ListMessagesController
from lib.infrastructure.presenter.list_messages_presenter import ListMessagesPresenter


class ListMessagesFeatureContainer(BaseFeatureContainer):
    conversation_repository: Any = providers.Dependency()

    presenter = providers.Factory[ListMessagesOutputPort](ListMessagesPresenter)

    usecase = providers.Factory[ListMessagesInputPort](
        ListMessagesUseCase, conversation_repository=conversation_repository
    )

    controller = providers.Factory(
        ListMessagesController,
        usecase=usecase,
        presenter=presenter,
    )
