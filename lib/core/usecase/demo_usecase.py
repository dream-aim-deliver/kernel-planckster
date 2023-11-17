from lib.core.ports.primary.demo_ports import DemoInputPort
from lib.core.sdk.usecase_models import BaseErrorResponse
from lib.core.usecase_models.demo_usecase_models import DemoRequest, DemoResponse


class DemoUseCase(DemoInputPort):
    def execute(self, request: DemoRequest) -> DemoResponse | BaseErrorResponse:
        return DemoResponse(sum=sum(request.numbers))
