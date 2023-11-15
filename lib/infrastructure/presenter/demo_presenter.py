from lib.core.ports.primary.demo_ports import DemoOutputPort
from lib.core.sdk.usecase_models import BaseErrorResponse
from lib.core.usecase_models.demo_usecase_models import DemoResponse
from lib.core.view_model.demo_view_model import DemoViewModel


class DemoPresenter(DemoOutputPort[DemoResponse, BaseErrorResponse, DemoViewModel]):
    def convert_response_to_view_model(self, response: DemoResponse) -> DemoViewModel:
        return DemoViewModel(status=True, code=200, sum=response.sum)

    def convert_error_response_to_view_model(self, response: BaseErrorResponse) -> DemoViewModel:
        return DemoViewModel(
            status=False,
            sum=0,
            code=response.errorCode,
            errorCode=response.errorCode,
            errorMessage=response.errorMessage,
            errorName=response.errorName,
            errorType=response.errorType,
        )
