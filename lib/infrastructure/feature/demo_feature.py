from typing import Annotated, Any, Dict, Literal, Type

from fastapi import Depends, Request, Response

from lib.core.sdk.caps_fastapi import FastAPIFeature
from lib.core.sdk.controller import BaseController
from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase_models import BaseErrorResponse
from lib.core.usecase_models.demo_usecase_models import DemoRequest, DemoResponse
from lib.core.view_model.demo_view_model import DemoViewModel
from lib.infrastructure.controller.demo_controller import DemoController, DemoControllerParameters
from lib.infrastructure.presenter.demo_presenter import DemoPresenter


class DemoFeature(
    FastAPIFeature[DemoControllerParameters, DemoRequest, DemoResponse, BaseErrorResponse, DemoViewModel]
):
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

    def presenter_factory(self) -> BasePresenter[DemoResponse, BaseErrorResponse, DemoViewModel]:
        return DemoPresenter()

    def controller_factory(
        self,
    ) -> BaseController[DemoControllerParameters, DemoRequest, DemoResponse, BaseErrorResponse, DemoViewModel]:
        return DemoController()

    def endpoint_fn(  # type: ignore
        self,
        request: Request,
        response: Response,
        request_query_parameters: Annotated[DemoControllerParameters, Depends()],
        # request_body_parameters: DemoControllerParameters,
    ) -> DemoViewModel:
        # Make controller parameters here with your FastAPI request parameters
        controllerParameters: DemoControllerParameters = request_query_parameters
        return self.handle_request(
            controller_parameters=controllerParameters,
        )
