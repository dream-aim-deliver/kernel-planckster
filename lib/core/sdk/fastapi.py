from abc import ABC, abstractmethod
from typing import Any, Generic, List, Literal
from fastapi import APIRouter, FastAPI
from lib.core.sdk.controller import BaseController, TBaseControllerParameters
from lib.core.sdk.feature import BaseFeature
from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase import BaseUseCase
from lib.core.sdk.usecase_models import TBaseRequest, TBaseResponse, TBaseErrorResponse
from lib.core.sdk.viewmodel import TBaseViewModel


class FastAPIFeature(
    ABC,
    # TODO: Is this needed?
    # Generic[TBaseControllerParameters, TBaseRequest, TBaseResponse, TBaseErrorResponse, TBaseViewModel],
    BaseFeature[TBaseControllerParameters, TBaseRequest, TBaseResponse, TBaseErrorResponse, TBaseViewModel],
):
    def __init__(
        self,
        app: FastAPI,
        name: str,
        description: str,
        version: str,
        verb: Literal["GET", "POST", "PUT", "DELETE"],
        endpoint: str,
        usecase: BaseUseCase[TBaseRequest, TBaseResponse, TBaseErrorResponse],
        controller: BaseController[TBaseControllerParameters, TBaseRequest],
        presenter: BasePresenter[TBaseResponse, TBaseErrorResponse, TBaseViewModel],
        auth_required: bool = False,
        enabled: bool = True,
    ) -> None:
        super().__init__(
            name, description, version, verb, endpoint, usecase, controller, presenter, auth_required, enabled
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
            async def get(controllerParameters: TBaseControllerParameters) -> TBaseViewModel:
                return self.controller.execute(controllerParameters)

        elif self.verb == "POST":

            @self.router.post(self.endpoint)
            async def post(controllerParameters: TBaseControllerParameters) -> TBaseViewModel:
                return self.controller.execute(controllerParameters)

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

    def load(self) -> None:
        super().load()
        self.routes()
        self.register_router()
