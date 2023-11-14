from abc import ABC, abstractmethod
from typing import Any, Generic, List, Literal, Type, TypeVar
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
from lib.core.sdk.controller import (
    BaseController,
    BaseControllerParameters,
    DummyController,
    DummyControllerParameters,
    TBaseControllerParameters,
    # TBaseController,
)
from lib.core.sdk.feature import BaseFeature
from lib.core.sdk.presenter import BasePresenter, DummyPresenter, DummyViewModel, TBasePresenter
from lib.core.sdk.usecase import (
    BaseUseCase,
    DummyErrorResponse,
    DummyRequest,
    DummyResponse,
    DummyUseCase,
    TBaseUseCase,
)
from lib.core.sdk.usecase_models import (
    BaseErrorResponse,
    BaseRequest,
    BaseResponse,
    TBaseRequest,
    TBaseResponse,
    TBaseErrorResponse,
)
from lib.core.sdk.viewmodel import BaseViewModel, TBaseViewModel


class FastAPIFeature(
    ABC,
    BaseFeature[
        TBaseControllerParameters,
        TBaseRequest,
        TBaseResponse,
        TBaseErrorResponse,
        TBaseViewModel,
        # TBaseController,
        TBaseUseCase,
        TBasePresenter,
    ],
):
    def __init__(
        self,
        app: FastAPI,
        name: str,
        description: str,
        version: str,
        verb: Literal["GET", "POST", "PUT", "DELETE"],
        endpoint: str,
        controller: type[BaseController[TBaseControllerParameters, TBaseRequest]],
        usecase: type[TBaseUseCase],
        presenter: type[TBasePresenter],
        auth_required: bool = False,
        enabled: bool = True,
    ) -> None:
        super().__init__(
            name, description, version, verb, endpoint, controller, usecase, presenter, auth_required, enabled
        )
        self._router: APIRouter | None = None
        self._app: FastAPI = app

    def _prepare_router(self) -> APIRouter:
        dependencies: List[Any] = []

        # if self.auth_required:
        #     dependencies = [with_auth]

        router = APIRouter(
            prefix=f"/{self.name}/{self.version}",
            tags=[self.name],
            dependencies=dependencies,
            responses={},
        )
        return router

    @property
    def router(self) -> APIRouter:
        if self._router is None:
            self._router = self._prepare_router()
        return self._router

    def routes(self) -> None:
        if self.verb == "GET":

            @self.router.get(self.endpoint)
            def get(controllerParameters: TBaseControllerParameters) -> TBaseViewModel:
                output = self.controller.execute(controllerParameters)
                if output is None:
                    raise Exception("Output is None")
                return output

        elif self.verb == "POST":

            @self.router.post(self.endpoint)
            def post(controllerParameters: TBaseControllerParameters) -> TBaseViewModel:
                output = self.controller.execute(controllerParameters)
                if output is None:
                    raise Exception("Output is None")
                return output

        # elif self.verb == "PUT":

        #     @self.router.put(self.endpoint)
        #     async def put() -> Any:
        #         return self.execute()

        # elif self.verb == "DELETE":

        #     @self.router.delete(self.endpoint)
        #     async def delete() -> Any:
        #         return self.execute()

    def register_router(self) -> None:
        self._app.include_router(self.router)

    def register(self) -> None:
        super().register()
        self.routes()
        self.register_router()


class DummyFeature(
    FastAPIFeature[
        DummyControllerParameters,
        DummyRequest,
        DummyResponse,
        DummyErrorResponse,
        DummyViewModel,
        # DummyController,
        DummyUseCase,
        DummyPresenter,
    ]
):
    def __init__(
        self,
        enabled: bool = True,
    ) -> None:
        super().__init__(
            FastAPI(),
            "dummy feature",
            "multiples a number by 2",
            "1.0",
            "GET",
            "/dummy",
            DummyController,
            DummyUseCase,
            DummyPresenter,
            False,
            enabled,
        )


class BaseDataStructure(BaseModel):
    pass


TBaseDataStructure = TypeVar("TBaseDataStructure", bound=BaseDataStructure)


class TestDataStructure(BaseDataStructure):
    id: int | None = None
    name: str | None = None


class TestBaseController(ABC, Generic[TBaseDataStructure]):
    def __init__(self, data: TBaseDataStructure) -> None:
        super().__init__()
        self._data = data

    @property
    def data(self) -> TBaseDataStructure:
        return self._data


class TestController(TestBaseController[TestDataStructure]):
    def __init__(self, id: int, name: str, data: TestDataStructure) -> None:
        super().__init__(data)
        self._id = id
        self._name = name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name


class SuperController(TestController):
    def __init__(self, id: int, name: str, data: TestDataStructure) -> None:
        super().__init__(id, name, data)


class TestBaseFeature(Generic[TBaseDataStructure]):
    def __init__(self, controller: TestBaseController[TBaseDataStructure]) -> None:
        self._controller = controller


class TestSuperFeature(TestBaseFeature[TestDataStructure]):
    def __init__(self, controller: SuperController) -> None:
        super().__init__(controller)


feature = TestSuperFeature(Super(1, "test", TestDataStructure(id=1, name="test")))
