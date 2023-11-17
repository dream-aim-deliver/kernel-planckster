from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, Generic, TypeVar
from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel
from lib.core.sdk.controller import BaseController, TBaseControllerParameters
from lib.core.sdk.feature import BaseFeatureDescriptor

from lib.core.sdk.viewmodel import (
    TBaseViewModel,
)

TQueryParameters = TypeVar("TQueryParameters", bound=BaseModel)
TBodyParameters = TypeVar("TBodyParameters", bound=BaseModel)


class FastAPIFeature(ABC, Generic[TQueryParameters, TBodyParameters, TBaseControllerParameters, TBaseViewModel]):
    def __init__(
        self,
        name: str,
        controller: BaseController[TBaseControllerParameters, Any, Any, Any, TBaseViewModel],
        descriptor: BaseFeatureDescriptor,
        responses: Dict[int | str, dict[str, Any]],
    ) -> None:
        self._name = name
        self._controller = controller
        self._descriptor = descriptor
        self._responses: Dict[int | str, dict[str, Any]] = responses

        tags: list[str | Enum] = [name]
        if self._descriptor.auth:
            tags.append("Protectected Endpoints")
        else:
            tags.append("Public Endpoints")

        self._router: APIRouter = APIRouter(
            prefix=f"/{name.lower()}",
            tags=tags,
        )

    @property
    def name(self) -> str:
        return self._name

    @property
    def controller(
        self,
    ) -> BaseController[TBaseControllerParameters, Any, Any, Any, TBaseViewModel]:
        return self._controller

    @property
    def descriptor(self) -> BaseFeatureDescriptor:
        return self._descriptor

    @property
    def responses(self) -> Dict[int | str, dict[str, Any]]:
        return self._responses

    @property
    def router(self) -> APIRouter:
        return self._router

    def register_routes(self) -> None:
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
            self.register_routes()
            return self.router
        else:
            return None

    @abstractmethod
    def create_controller_parameters(
        self, query: TQueryParameters | None, body: TBodyParameters | None
    ) -> TBaseControllerParameters:
        raise NotImplementedError("You must implement the create_controller_parameters method in your feature")

    def endpoint_fn(
        self,
        request: Request,
        response: Response,
        request_query_parameters: TQueryParameters | None = None,
        request_body_parameters: TBodyParameters | None = None,
    ) -> TBaseViewModel:
        controller_parameters: TBaseControllerParameters = self.create_controller_parameters(
            query=request_query_parameters,
            body=request_body_parameters,
        )
        view_model: TBaseViewModel | None = self.controller.execute(
            parameters=controller_parameters,
        )
        if view_model is None:
            raise HTTPException(500, "View model is None")
        else:
            response.status_code = view_model.code
            return view_model
