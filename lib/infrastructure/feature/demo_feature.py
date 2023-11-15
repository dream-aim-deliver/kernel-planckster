from typing import Annotated, Any, Dict, Literal, Type

from fastapi import Depends, Request, Response

from lib.core.sdk.caps_fastapi import FastAPIFeature
from lib.core.sdk.controller import BaseController, BaseControllerParameters
from lib.core.sdk.presenter import Presentable
from lib.core.sdk.usecase_models import BaseRequest
from lib.core.view_model.demo_view_model import DemoViewModel
from lib.infrastructure.presenter.demo_presenter import DemoPresenter


class DemoControllerParameters(BaseControllerParameters):
    num1: int
    num2: int


class DemoRequest(BaseRequest):
    numbers: list[int]


class DemoController(BaseController[DemoControllerParameters, DemoRequest, DemoViewModel]):
    def __init__(self) -> None:
        super().__init__(presenter=DemoPresenter())

    def create_request(self, parameters: DemoControllerParameters) -> DemoRequest:
        return DemoRequest(numbers=[parameters.num1, parameters.num2])


class DemoFeature(FastAPIFeature[DemoControllerParameters, DemoRequest, DemoViewModel]):
    name: str = "Demo Feature"
    version: str = "1.0.0"
    description: str = "Adds 2 numbers"
    group: str = "demo"
    verb: Literal["GET", "POST", "PUT", "DELETE"] = "GET"
    endpoint: str = "/endpoint"
    responses: Dict[int | str, dict[str, Any]] = {
        200: {
            "model": DemoViewModel,
            "description": "Success",
        },
        500: {
            "model": DemoViewModel,
            "description": "Internal Server Error",
        },
    }

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

    def presenter_factory(self) -> Presentable[DemoViewModel]:
        return DemoPresenter()

    def controller_factory(self) -> BaseController[DemoControllerParameters, DemoRequest, DemoViewModel]:
        return DemoController()

    def endpoint_fn(  # type: ignore
        self,
        request: Request,
        response: Response,
        request_query_parameters: Annotated[DemoControllerParameters, Depends()],
        # request_body_parameters: DemoControllerParameters,
        # parameters: DemoControllerParameters,
    ) -> DemoViewModel:
        return super().endpoint_fn(
            request=request,
            response=response,
            request_query_parameters=request_query_parameters,
            # request_body_parameters=request_body_parameters,
        )
