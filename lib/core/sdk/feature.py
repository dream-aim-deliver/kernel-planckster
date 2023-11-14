from typing import Generic, Literal, Type

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
    Generic[
        TBaseControllerParameters,
        TBaseRequest,
        TBaseResponse,
        TBaseErrorResponse,
        TBaseViewModel,
        # TBaseController,
        TBaseUseCase,
        TBasePresenter,
    ]
):
    def __init__(
        self,
        name: str,
        description: str,
        version: str,
        verb: Literal["GET", "POST", "PUT", "DELETE"],
        endpoint: str,
        controller: type[BaseController[TBaseControllerParameters, TBaseRequest]],
        usecase: type[BaseUseCase[TBaseRequest, TBaseResponse, TBaseErrorResponse]],
        presenter: type[BasePresenter[TBaseResponse, TBaseErrorResponse, TBaseViewModel]],
        auth_required: bool = False,
        enabled: bool = True,
    ) -> None:
        self._name = name
        self._description = description
        self._version = version
        self._verb = verb
        self._endpoint = endpoint
        self._auth_required = auth_required
        self._enabled = enabled
        self._usecase = usecase()
        self._presenter = presenter()
        self._controller = controller(self._usecase, self._presenter)

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value

    @property
    def version(self) -> str:
        return self._version

    @property
    def verb(self) -> Literal["GET", "POST", "PUT", "DELETE"]:
        return self._verb

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @property
    def auth_required(self) -> bool:
        return self._auth_required

    @property
    def controller(self) -> BaseController[TBaseControllerParameters, TBaseRequest]:
        return self._controller

    @property
    def usecase(self) -> BaseUseCase[TBaseRequest, TBaseResponse, TBaseErrorResponse]:
        return self._usecase

    @property
    def presenter(self) -> BasePresenter[TBaseResponse, TBaseErrorResponse, TBaseViewModel]:
        return self._presenter

    def __str__(self) -> str:
        return f"{self.name} ({self.version})"

    def __repr__(self) -> str:
        return f"{self.name} ({self.version})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseFeature):
            return NotImplemented
        return self.name == other.name and self.version == other.version

    def __hash__(self) -> int:
        return hash((self.name, self.version))

    def register(self) -> None:
        if not self.enabled:
            raise Exception(f"Cannot load {self}. Feature {self} is disabled")

    def execute(self, parameters: TBaseControllerParameters) -> TBaseViewModel | None:
        return self.controller.execute(parameters)
