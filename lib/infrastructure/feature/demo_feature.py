from typing import Any, Literal

from fastapi import HTTPException, Request, Response
from lib.core.sdk.caps_fastapi import FastAPIFeature
from lib.core.sdk.presenter import Presentable
from lib.core.sdk.usecase_models import BaseErrorResponse
from lib.core.view_model.demo_view_model import DemoViewModel
from lib.infrastructure.presenter.demo_presenter import DemoPresenter


class DemoFeature(FastAPIFeature[DemoViewModel]):
    name: str = "Demo"
    description: str = "Demo Feature"
    group: str = "demo"
    verb: Literal["GET", "POST", "PUT", "DELETE"] = "GET"
    endpoint: str = "/endpoint"
    presenter: Presentable[DemoViewModel] = DemoPresenter()

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

    def endpoint_fn(self, request: Request, response: Response) -> DemoViewModel:
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
