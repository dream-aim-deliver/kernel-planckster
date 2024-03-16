from abc import abstractmethod
from lib.core.ports.secondary.research_context_repository import ResearchContextRepositoryOutputPort
from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase import BaseUseCase
from lib.core.usecase_models.list_source_data_for_research_context_usecase_models import (
    ListSourceDataForResearchContextError,
    ListSourceDataForResearchContextRequest,
    ListSourceDataForResearchContextResponse,
)
from lib.core.view_model.list_source_data_for_research_context_view_model import (
    ListSourceDataForResearchContextViewModel,
)


class ListSourceDataForResearchContextInputPort(
    BaseUseCase[
        ListSourceDataForResearchContextRequest,
        ListSourceDataForResearchContextResponse,
        ListSourceDataForResearchContextError,
    ]
):
    def __init__(self, research_context_repository: ResearchContextRepositoryOutputPort) -> None:
        self._research_context_repository = research_context_repository

    @property
    def research_context_repository(self) -> ResearchContextRepositoryOutputPort:
        return self._research_context_repository

    @abstractmethod
    def execute(
        self, request: ListSourceDataForResearchContextRequest
    ) -> ListSourceDataForResearchContextResponse | ListSourceDataForResearchContextError:
        raise NotImplementedError("This method must be implemented by the usecase.")


class ListSourceDataForResearchContextOutputPort(
    BasePresenter[
        ListSourceDataForResearchContextResponse,
        ListSourceDataForResearchContextError,
        ListSourceDataForResearchContextViewModel,
    ]
):
    @abstractmethod
    def convert_error_response_to_view_model(
        self, response: ListSourceDataForResearchContextError
    ) -> ListSourceDataForResearchContextViewModel:
        raise NotImplementedError(
            "You must implement the convert_error_response_to_view_model method in your presenter"
        )

    @abstractmethod
    def convert_response_to_view_model(
        self, response: ListSourceDataForResearchContextResponse
    ) -> ListSourceDataForResearchContextViewModel:
        raise NotImplementedError("You must implement the convert_response_to_view_model method in your presenter")
