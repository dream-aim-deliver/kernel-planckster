from abc import abstractmethod
from lib.core.ports.secondary.client_repository import ClientRepositoryOutputPort
from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase import BaseUseCase
from lib.core.usecase_models.list_source_data_usecase_models import (
    ListSourceDataError,
    ListSourceDataRequest,
    ListSourceDataResponse,
)
from lib.core.view_model.list_source_data_view_model import ListSourceDataViewModel


class ListSourceDataInputPort(BaseUseCase[ListSourceDataRequest, ListSourceDataResponse, ListSourceDataError]):
    def __init__(self, client_repository: ClientRepositoryOutputPort) -> None:
        self._client_repository = client_repository

    @property
    def client_repository(self) -> ClientRepositoryOutputPort:
        return self._client_repository

    @abstractmethod
    def execute(self, request: ListSourceDataRequest) -> ListSourceDataResponse | ListSourceDataError:
        raise NotImplementedError("This method must be implemented by the usecase.")


class ListSourceDataOutputPort(BasePresenter[ListSourceDataResponse, ListSourceDataError, ListSourceDataViewModel]):
    @abstractmethod
    def convert_error_response_to_view_model(self, response: ListSourceDataError) -> ListSourceDataViewModel:
        raise NotImplementedError(
            "You must implement the convert_error_response_to_view_model method in your presenter"
        )

    @abstractmethod
    def convert_response_to_view_model(self, response: ListSourceDataResponse) -> ListSourceDataViewModel:
        raise NotImplementedError("You must implement the convert_response_to_view_model method in your presenter")
