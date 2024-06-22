from abc import abstractmethod
from lib.core.ports.secondary.client_repository import ClientRepositoryOutputPort
from lib.core.ports.secondary.research_context_repository import ResearchContextRepositoryOutputPort
from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase import BaseUseCase
from lib.core.usecase_models.extend_research_context_usecase_models import (
    ExtendResearchContextError,
    ExtendResearchContextRequest,
    ExtendResearchContextResponse,
)
from lib.core.view_model.new_research_context_view_mode import NewResearchContextViewModel


class ExtendResearchContextInputPort(
    BaseUseCase[ExtendResearchContextRequest, ExtendResearchContextResponse, ExtendResearchContextError]
):
    def __init__(
        self,
        client_repository: ClientRepositoryOutputPort,
        research_context_repository: ResearchContextRepositoryOutputPort,
    ) -> None:
        self._client_repository = client_repository
        self._research_context_repository = research_context_repository

    @property
    def client_repository(self) -> ClientRepositoryOutputPort:
        return self._client_repository

    @property
    def research_context_repository(self) -> ResearchContextRepositoryOutputPort:
        return self._research_context_repository

    @abstractmethod
    def execute(
        self, request: ExtendResearchContextRequest
    ) -> ExtendResearchContextResponse | ExtendResearchContextError:
        raise NotImplementedError("This method must be implemented by the usecase.")


class ExtendResearchContextOutputPort(
    BasePresenter[ExtendResearchContextResponse, ExtendResearchContextError, NewResearchContextViewModel]
):
    @abstractmethod
    def convert_error_response_to_view_model(self, response: ExtendResearchContextError) -> NewResearchContextViewModel:
        raise NotImplementedError(
            "You must implement the convert_error_response_to_view_model method in your presenter"
        )

    @abstractmethod
    def convert_response_to_view_model(self, response: ExtendResearchContextResponse) -> NewResearchContextViewModel:
        raise NotImplementedError("You must implement the convert_response_to_view_model method in your presenter")
