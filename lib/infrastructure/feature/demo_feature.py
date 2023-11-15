from typing import Any, Dict, Literal

from lib.core.sdk.caps_fastapi import FastAPIFeature
from lib.core.sdk.controller import BaseControllerParameters
from lib.core.sdk.presenter import Presentable
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
    # presenter: Presentable[DemoViewModel] = DemoPresenter()

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

    def presenter_factory(self) -> Presentable[DemoViewModel]:
        return DemoPresenter()
