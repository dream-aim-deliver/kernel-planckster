from enum import Enum
from typing import Annotated, Any, Dict

from fastapi import APIRouter, Depends, Request, Response

from lib.core.sdk.feature import BaseFeatureDescriptor
from lib.core.view_model.demo_view_model import DemoViewModel
from lib.infrastructure.controller.demo_controller import DemoController, DemoControllerParameters
from lib.infrastructure.config.containers import ApplicationContainer

from dependency_injector.wiring import inject, Provide


class DemoFastAPIFeature:
    @inject
    def __init__(
        self,
        descriptor_provider: Any = Provide[ApplicationContainer.features.demo.feature_descriptor.provider],  # type: ignore
        controller_provider: Any = Provide[ApplicationContainer.features.demo.controller.provider],  # type: ignore
    ) -> None:
        self._descriptor: BaseFeatureDescriptor = descriptor_provider()
        tags: list[str | Enum] = [self._descriptor.name]
        if self._descriptor.auth:
            tags.append("auth_required")
        # TODO - if auth is required, then add a dependency to token validator fn in the router description below. See https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/?
        self._router: APIRouter = APIRouter(
            prefix="/demo",
            tags=tags,
        )
        self._controller: DemoController = controller_provider()
        self._responses: Dict[int | str, dict[str, Any]] = {
            200: {
                "model": DemoViewModel,
                "description": "Success",
            },
            500: {
                "model": DemoViewModel,
                "description": "Internal Server Error",
            },
        }

    @property
    def descriptor(self) -> BaseFeatureDescriptor:
        return self._descriptor

    @property
    def responses(self) -> Dict[int | str, dict[str, Any]]:
        return self._responses

    @property
    def router(self) -> APIRouter:
        return self._router

    @property
    def controller(self) -> DemoController:
        return self._controller

    def routes(self) -> None:
        self.router.add_api_route(
            name=self.descriptor.name,
            description=self.descriptor.description,
            methods=[self.descriptor.verb],
            path=self.descriptor.endpoint,
            endpoint=self.endpoint_fn,
            responses=self.responses,
        )

    def load(self) -> APIRouter | None:
        if self.descriptor.enabled:
            self.routes()
            return self.router
        else:
            return None

    def endpoint_fn(
        self,
        request: Request,
        response: Response,
        request_query_parameters: Annotated[DemoControllerParameters, Depends()],
        # request_body_parameters: DemoControllerParameters,
    ) -> DemoViewModel | None:
        # Make controller parameters here with your FastAPI request parameters
        controllerParameters: DemoControllerParameters = request_query_parameters
        view_model: DemoViewModel | None = self.controller.execute(controllerParameters)
        if view_model is None:
            return None
        else:
            response.status_code = view_model.code
            return view_model
