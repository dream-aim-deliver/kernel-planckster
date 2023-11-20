from abc import abstractmethod
from lib.core.ports.secondary.user_repository import UserRepositoryOutputPort
from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase import BaseUseCase
from lib.core.usecase_models.new_research_context_usecase_models import (
    NewResearchContextError,
    NewResearchContextRequest,
    NewResearchContextResponse,
)
from lib.core.view_model.new_research_context_view_mode import NewResearchContextViewModel


class NewResearchContextInputPort(
    BaseUseCase[NewResearchContextRequest, NewResearchContextResponse, NewResearchContextError]
):
    def __init__(self, user_repository: UserRepositoryOutputPort) -> None:
        self._user_repository = user_repository

    @property
    def user_repository(self) -> UserRepositoryOutputPort:
        return self._user_repository

    @abstractmethod
    def execute(self, request: NewResearchContextRequest) -> NewResearchContextResponse | NewResearchContextError:
        raise NotImplementedError("This method must be implemented by the usecase.")


class NewResearchContextOutputPort(
    BasePresenter[NewResearchContextResponse, NewResearchContextError, NewResearchContextViewModel]
):
    @abstractmethod
    def convert_error_response_to_view_model(self, response: NewResearchContextError) -> NewResearchContextViewModel:
        raise NotImplementedError(
            "You must implement the convert_error_response_to_view_model method in your presenter"
        )

    @abstractmethod
    def convert_response_to_view_model(self, response: NewResearchContextResponse) -> NewResearchContextViewModel:
        raise NotImplementedError("You must implement the convert_response_to_view_model method in your presenter")
