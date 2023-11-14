from typing import Generic, Literal, Type

from pydantic import BaseModel

from lib.core.sdk.controller import (
    BaseController,
    DummyController,
    DummyControllerParameters,
    # TBaseController,
    TBaseControllerParameters,
)
from lib.core.sdk.presenter import BasePresenter, DummyPresenter, DummyViewModel, TBasePresenter
from lib.core.sdk.usecase import (
    BaseUseCase,
    DummyErrorResponse,
    DummyRequest,
    DummyResponse,
    DummyUseCase,
    TBaseUseCase,
)
from lib.core.sdk.usecase_models import TBaseRequest, TBaseResponse, TBaseErrorResponse
from lib.core.sdk.viewmodel import TBaseViewModel


class BaseFeature(
    BaseModel,
    Generic[
        TBaseControllerParameters,
        TBaseRequest,
        TBaseResponse,
        TBaseErrorResponse,
        TBaseViewModel,
    ],
):
    name: str
    description: str
    version: str
    verb: Literal["GET", "POST", "PUT", "DELETE"]
    endpoint: str
    controller: BaseController[TBaseControllerParameters, TBaseRequest]
    usecase: BaseUseCase[TBaseRequest, TBaseResponse, TBaseErrorResponse]
    presenter: BasePresenter[TBaseResponse, TBaseErrorResponse, TBaseViewModel]
    auth_required: bool = False
    enabled: bool = True

    def register(self) -> None:
        if not self.enabled:
            raise Exception(f"Cannot load {self}. Feature {self} is disabled")

    def execute(self, parameters: TBaseControllerParameters) -> TBaseViewModel | None:
        return self.controller.execute(parameters)
