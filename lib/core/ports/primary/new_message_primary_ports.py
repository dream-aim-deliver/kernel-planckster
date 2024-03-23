from abc import abstractmethod
from lib.core.ports.secondary.conversation_repository import ConversationRepository
from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase import BaseUseCase
from lib.core.usecase_models.new_message_usecase_models import NewMessageError, NewMessageRequest, NewMessageResponse
from lib.core.view_model.new_message_view_model import NewMessageViewModel


class NewMessageInputPort(BaseUseCase[NewMessageRequest, NewMessageResponse, NewMessageError]):
    def __init__(
        self,
        conversation_repository: ConversationRepository,
    ) -> None:
        self._conversation_repository = conversation_repository

    @property
    def conversation_repository(self) -> ConversationRepository:
        return self._conversation_repository

    @abstractmethod
    def execute(
        self,
        request: NewMessageRequest,
    ) -> NewMessageResponse | NewMessageError:
        raise NotImplementedError("This method must be implemented by the usecase.")


class NewMessageOutputPort(
    BasePresenter[
        NewMessageResponse,
        NewMessageError,
        NewMessageViewModel,
    ]
):
    @abstractmethod
    def convert_error_response_to_view_model(
        self,
        response: NewMessageError,
    ) -> NewMessageViewModel:
        raise NotImplementedError(
            "You must implement the convert_error_response_to_view_model method in your presenter"
        )

    @abstractmethod
    def convert_response_to_view_model(
        self,
        response: NewMessageResponse,
    ) -> NewMessageViewModel:
        raise NotImplementedError("You must implement the convert_response_to_view_model method in your presenter")
