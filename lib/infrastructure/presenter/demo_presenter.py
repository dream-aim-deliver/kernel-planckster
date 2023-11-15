from lib.core.sdk.usecase_models import BaseErrorResponse, BaseResponse
from lib.core.view_model.demo_view_model import DemoViewModel


class DemoPresenter:
    def present_success(self, response: BaseResponse) -> DemoViewModel:
        return DemoViewModel(status=True, code=200, id=1, test="This is a test")

    def present_error(self, response: BaseErrorResponse) -> DemoViewModel:
        return DemoViewModel(
            status=False,
            code=response.errorCode,
            errorCode=response.errorCode,
            errorMessage=response.errorMessage,
            errorName=response.errorName,
            errorType=response.errorType,
        )
