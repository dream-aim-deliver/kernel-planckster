from typing import Any
from lib.core.ports.primary.new_conversation_primary_ports import NewConversationInputPort, NewConversationOutputPort
from lib.core.sdk.ioc_feature_container import BaseFeatureContainer

from dependency_injector import providers
from lib.core.usecase.new_conversation_usecase import NewConversationUseCase
from lib.infrastructure.controller.new_conversation_controller import NewConversationController

from lib.infrastructure.presenter.new_conversation_presenter import NewConversationPresenter


class NewConversationFeatureContainer(BaseFeatureContainer):
    research_context_repository: Any = providers.Dependency()

    presenter = providers.Factory[NewConversationOutputPort](NewConversationPresenter)

    usecase = providers.Factory[NewConversationInputPort](
        NewConversationUseCase, research_context_repository=research_context_repository
    )

    controller = providers.Factory(
        NewConversationController,
        usecase=usecase,
        presenter=presenter,
    )
