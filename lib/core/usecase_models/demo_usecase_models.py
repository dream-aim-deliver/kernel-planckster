from lib.core.sdk.usecase_models import BaseRequest, BaseResponse


class DemoRequest(BaseRequest):
    numbers: list[int]


class DemoResponse(BaseResponse):
    sum: int
