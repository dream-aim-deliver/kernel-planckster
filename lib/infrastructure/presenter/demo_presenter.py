from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase_models import BaseErrorResponse
from lib.core.usecase_models.demo_usecase_models import DemoResponse
from lib.core.view_model.demo_view_model import DemoViewModel


class DemoPresenter(BasePresenter[DemoResponse, BaseErrorResponse, DemoViewModel]):
    def present_success(self, response: DemoResponse) -> DemoViewModel:
        return DemoViewModel(status=True, code=200, sum=response.sum)

    def present_error(self, response: BaseErrorResponse) -> DemoViewModel:
        return DemoViewModel(
            status=False,
            sum=0,
            code=response.errorCode,
            errorCode=response.errorCode,
            errorMessage=response.errorMessage,
            errorName=response.errorName,
            errorType=response.errorType,
        )
