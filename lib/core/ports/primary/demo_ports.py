from abc import abstractmethod
from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase import BaseUseCase

from lib.core.sdk.usecase_models import BaseErrorResponse
from lib.core.usecase_models.demo_usecase_models import DemoRequest, DemoResponse
from lib.core.view_model.demo_view_model import DemoViewModel


class DemoInputPort(BaseUseCase[DemoRequest, DemoResponse, BaseErrorResponse]):
    @abstractmethod
    def execute(self, request: DemoRequest) -> DemoResponse | BaseErrorResponse:
        raise NotImplementedError("This method must be implemented by the usecase.")


class DemoOutputPort(
    BasePresenter[DemoResponse, BaseErrorResponse, DemoViewModel],
):
    @abstractmethod
    def convert_error_response_to_view_model(self, response: BaseErrorResponse) -> DemoViewModel:
        raise NotImplementedError(
            "You must implement the convert_error_response_to_view_model method in your presenter"
        )

    @abstractmethod
    def convert_response_to_view_model(self, response: DemoResponse) -> DemoViewModel:
        raise NotImplementedError("You must implement the convert_response_to_view_model method in your presenter")
