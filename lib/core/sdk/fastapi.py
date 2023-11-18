from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, Generic
from fastapi import APIRouter, HTTPException
from lib.core.sdk.controller import BaseController, TBaseControllerParameters
from lib.core.sdk.feature_descriptor import BaseFeatureDescriptor

from lib.core.sdk.viewmodel import (
    TBaseViewModel,
)


class FastAPIEndpoint(ABC, Generic[TBaseControllerParameters, TBaseViewModel]):
    def __init__(
        self,
        controller: BaseController[TBaseControllerParameters, Any, Any, Any, TBaseViewModel],
        descriptor: BaseFeatureDescriptor,
        responses: Dict[int | str, dict[str, Any]],
    ) -> None:
        name = descriptor.name
        self._name = name
        self._controller = controller
        self._descriptor = descriptor
        self._responses: Dict[int | str, dict[str, Any]] = responses

        tags: list[str | Enum] = [name]
        tags.extend(descriptor.tags)
        if self._descriptor.auth:
            tags.append("Protectected Endpoints")
        else:
            tags.append("Public Endpoints")

        self._router: APIRouter = APIRouter(
            prefix=f"/api/v1",
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

    def load(self) -> APIRouter | None:
        if self.descriptor.enabled:
            self.register_endpoint()
            return self.router
        else:
            return None

    @abstractmethod
    def register_endpoint(self) -> None:
        raise NotImplementedError("You must implement the register_endpoint method in your FastAPI endpoint subclass")

    def execute(self, controller_parameters: TBaseControllerParameters) -> TBaseViewModel:
        try:
            view_model = self.controller.execute(controller_parameters)
            if view_model is None:
                raise HTTPException(status_code=500, detail="Internal Server Error. Did not receive a view model")
            else:
                return view_model
        except Exception as e:
            raise e
