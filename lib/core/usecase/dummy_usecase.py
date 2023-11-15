from lib.core.sdk.usecase import BaseUseCase
from lib.core.sdk.usecase_models import BaseErrorResponse
from lib.core.usecase_models.demo_usecase_models import DemoRequest, DemoResponse


class DemoUseCase(BaseUseCase[DemoRequest, DemoResponse, BaseErrorResponse]):
    def execute(self, request: DemoRequest) -> DemoResponse | BaseErrorResponse:
        return DemoResponse(sum=sum(request.numbers))
