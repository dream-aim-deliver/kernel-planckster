from lib.core.sdk.controller import BaseController, BaseControllerParameters
from lib.core.sdk.usecase_models import BaseErrorResponse
from lib.core.usecase.demo_usecase import DemoUseCase
from lib.core.usecase_models.demo_usecase_models import DemoRequest, DemoResponse
from lib.core.view_model.demo_view_model import DemoViewModel
from lib.infrastructure.presenter.demo_presenter import DemoPresenter


class DemoControllerParameters(BaseControllerParameters):
    num1: int
    num2: int


class DemoController(
    BaseController[DemoControllerParameters, DemoRequest, DemoResponse, BaseErrorResponse, DemoViewModel]
):
    def __init__(self) -> None:
        super().__init__(usecase=DemoUseCase(), presenter=DemoPresenter())

    def create_request(self, parameters: DemoControllerParameters | None) -> DemoRequest:
        if parameters is None:
            return DemoRequest(numbers=[0, 0])
        else:
            return DemoRequest(numbers=[parameters.num1, parameters.num2])
