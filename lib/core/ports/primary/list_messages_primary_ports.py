from abc import abstractmethod
from lib.core.ports.secondary.conversation_repository import ConversationRepository
from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase import BaseUseCase
from lib.core.usecase_models.list_messages_usecase_models import (
    ListMessagesRequest,
    ListMessagesResponse,
    ListMessagesError,
)
from lib.core.view_model.list_messages_view_model import ListMessagesViewModel


class ListMessagesInputPort(
    BaseUseCase[
        ListMessagesRequest,
        ListMessagesResponse,
        ListMessagesError,
    ]
):
    def __init__(self, conversation_repository: ConversationRepository) -> None:
        self._conversation_repository = conversation_repository

    @property
    def conversation_repository(self) -> ConversationRepository:
        return self._conversation_repository

    @abstractmethod
    def execute(self, request: ListMessagesRequest) -> ListMessagesResponse | ListMessagesError:
        raise NotImplementedError("This method must be implemented by the usecase.")


class ListMessagesOutputPort(
    BasePresenter[
        ListMessagesResponse,
        ListMessagesError,
        ListMessagesViewModel,
    ]
):
    @abstractmethod
    def convert_error_response_to_view_model(self, response: ListMessagesError) -> ListMessagesViewModel:
        raise NotImplementedError(
            "You must implement the convert_error_response_to_view_model method in your presenter"
        )

    @abstractmethod
    def convert_response_to_view_model(self, response: ListMessagesResponse) -> ListMessagesViewModel:
        raise NotImplementedError("You must implement the convert_response_to_view_model method in your presenter")
