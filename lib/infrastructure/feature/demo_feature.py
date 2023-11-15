from typing import Any, Dict, Literal

from fastapi import HTTPException, Request, Response
from lib.core.sdk.caps_fastapi import FastAPIFeature
from lib.core.sdk.controller import BaseControllerParameters
from lib.core.sdk.presenter import Presentable
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest
from lib.core.view_model.demo_view_model import DemoViewModel
from lib.infrastructure.presenter.demo_presenter import DemoPresenter


class DemoControllerParameters(BaseControllerParameters):
    num1: int
    num2: int


class DemoFeature(FastAPIFeature[DemoViewModel]):
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
    presenter: Presentable[DemoViewModel] = DemoPresenter()

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

    def presenter_factory(self) -> Presentable[DemoViewModel]:
        return DemoPresenter()

    def endpoint_fn(
        self,
        request: Request,
        response: Response,
    ) -> DemoViewModel:
        presenter = self.presenter
        name = self.name
        if presenter is None:
            raise HTTPException(status_code=500, detail="Presenter is not defined")
        else:
            # data = presenter.present_success(response=BaseResponse(status=True, result="Hello World!"))
            data = presenter.present_error(
                BaseErrorResponse(
                    status=False, code=500, errorCode=500, errorMessage="Error", errorName="Error", errorType="Error"
                )
            )
            response.status_code = data.code
            return data
