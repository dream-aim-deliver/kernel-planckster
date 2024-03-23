from typing import Any
from lib.core.ports.primary.new_message_primary_ports import NewMessageInputPort, NewMessageOutputPort
from lib.core.sdk.ioc_feature_container import BaseFeatureContainer

from dependency_injector import providers

from lib.core.usecase.new_message_usecase import NewMessageUseCase
from lib.infrastructure.controller.new_message_controller import NewMessageController
from lib.infrastructure.presenter.new_message_presenter import NewMessagePresenter


class NewMessageFeatureContainer(BaseFeatureContainer):
    conversation_repository: Any = providers.Dependency()

    presenter = providers.Factory[NewMessageOutputPort](NewMessagePresenter)

    usecase = providers.Factory[NewMessageInputPort](NewMessageUseCase, conversation_repository=conversation_repository)

    controller = providers.Factory(
        NewMessageController,
        usecase=usecase,
        presenter=presenter,
    )
