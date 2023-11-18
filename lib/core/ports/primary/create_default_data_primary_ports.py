from abc import abstractmethod
from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase import BaseUseCase
from lib.core.usecase_models.create_default_data_usecase_models import (
    CreateDefaultDataError,
    CreateDefaultDataRequest,
    CreateDefaultDataResponse,
)
from lib.core.view_model.create_default_data_view_model import CreateDefaultDataViewModel


class CreateDefaultDataInputPort(
    BaseUseCase[CreateDefaultDataRequest, CreateDefaultDataResponse, CreateDefaultDataError]
):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def execute(self, request: CreateDefaultDataRequest) -> CreateDefaultDataResponse | CreateDefaultDataError:
        raise NotImplementedError("This method must be implemented by the usecase.")


class CreateDefaultDataOutputPort(
    BasePresenter[CreateDefaultDataResponse, CreateDefaultDataError, CreateDefaultDataViewModel]
):
    @abstractmethod
    def convert_error_response_to_view_model(self, response: CreateDefaultDataError) -> CreateDefaultDataViewModel:
        raise NotImplementedError(
            "You must implement the convert_error_response_to_view_model method in your presenter"
        )

    @abstractmethod
    def convert_response_to_view_model(self, response: CreateDefaultDataResponse) -> CreateDefaultDataViewModel:
        raise NotImplementedError("You must implement the convert_response_to_view_model method in your presenter")
