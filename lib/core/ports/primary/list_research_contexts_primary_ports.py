from abc import abstractmethod
from lib.core.ports.secondary.user_repository import UserRepositoryOutputPort
from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase import BaseUseCase
from lib.core.usecase_models.list_research_contexts_usecase_models import (
    ListResearchContextsError,
    ListResearchContextsRequest,
    ListResearchContextsResponse,
)
from lib.core.view_model.list_research_contexts_view_model import ListResearchContextsViewModel


class ListResearchContextsInputPort(
    BaseUseCase[ListResearchContextsRequest, ListResearchContextsResponse, ListResearchContextsError]
):
    def __init__(self, user_repository: UserRepositoryOutputPort) -> None:
        self._user_repository = user_repository

    @property
    def user_repository(self) -> UserRepositoryOutputPort:
        return self._user_repository

    @abstractmethod
    def execute(self, request: ListResearchContextsRequest) -> ListResearchContextsResponse | ListResearchContextsError:
        raise NotImplementedError("This method must be implemented by the usecase.")


class ListResearchContextsOutputPort(
    BasePresenter[ListResearchContextsResponse, ListResearchContextsError, ListResearchContextsViewModel]
):
    @abstractmethod
    def convert_error_response_to_view_model(
        self, response: ListResearchContextsError
    ) -> ListResearchContextsViewModel:
        raise NotImplementedError(
            "You must implement the convert_error_response_to_view_model method in your presenter"
        )

    @abstractmethod
    def convert_response_to_view_model(self, response: ListResearchContextsResponse) -> ListResearchContextsViewModel:
        raise NotImplementedError("You must implement the convert_response_to_view_model method in your presenter")
