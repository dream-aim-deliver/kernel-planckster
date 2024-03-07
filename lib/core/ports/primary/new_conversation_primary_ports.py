from abc import abstractmethod
from lib.core.ports.secondary.research_context_repository import ResearchContextRepositoryOutputPort
from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase import BaseUseCase
from lib.core.usecase_models.new_conversation_usecase_models import NewConversationError, NewConversationRequest, NewConversationResponse
from lib.core.view_model.new_conversation_view_model import NewConversationViewModel


class NewConversationInputPort(BaseUseCase[NewConversationRequest, NewConversationResponse, NewConversationError]):
    def __init__(self, research_context_repository: ResearchContextRepositoryOutputPort) -> None:
        self._research_context_repository = research_context_repository

    @property
    def research_context_repository(self) -> ResearchContextRepositoryOutputPort:
        return self._research_context_repository

    @abstractmethod
    def execute(self, request: NewConversationRequest) -> NewConversationResponse | NewConversationError:
        raise NotImplementedError("This method must be implemented by the usecase.")


class NewConversationOutputPort(BasePresenter[NewConversationResponse, NewConversationError, NewConversationViewModel ]):

    @abstractmethod
    def convert_error_response_to_view_model(self, response: NewConversationError) -> NewConversationViewModel:
        raise NotImplementedError(
            "You must implement the convert_error_response_to_view_model method in your presenter"
        )

    @abstractmethod
    def convert_response_to_view_model(self, response: NewConversationResponse) -> NewConversationViewModel:
        raise NotImplementedError("You must implement the convert_response_to_view_model method in your presenter")