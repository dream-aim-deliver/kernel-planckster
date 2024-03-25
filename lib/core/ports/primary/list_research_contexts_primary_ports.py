from abc import abstractmethod
from lib.core.ports.secondary.client_repository import ClientRepositoryOutputPort
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
    def __init__(self, client_repository: ClientRepositoryOutputPort) -> None:
        self._client_repository = client_repository

    @property
    def client_repository(self) -> ClientRepositoryOutputPort:
        return self._client_repository

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
