from abc import ABC, abstractmethod
from enum import Enum
from typing import Annotated, Any, Dict, Generic
from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import ValidationError
from lib.core.sdk.controller import BaseController, TBaseControllerParameters
from lib.core.sdk.feature_descriptor import BaseFeatureDescriptor
import logging

logger = logging.getLogger(__name__)

from lib.core.sdk.viewmodel import (
    BaseViewModel,
    TBaseViewModel,
)

from fastapi import status


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
            tags.append("protected")
        else:
            tags.append("public")

        self.prefix = f"/api/v1"
        router: APIRouter = APIRouter(
            tags=tags,
        )
        if self._descriptor.auth:
            router.dependencies.append(Depends(self.check_auth))

        self._router = router

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
        except ValidationError as ve:
            return self.controller.presenter.present_error(
                BaseViewModel(
                    status=False,
                    code=400,
                    errorCode=400,
                    errorMessage="Bad Request",
                    errorName="Bad Request",
                    errorType=f"ValidationError: {ve}",
                )
            )
        except Exception as e:
            logger.error(f"Critical Error in {self.name} endpoint. See the following exception: {e}")
            raise e

    def check_auth(self, x_auth_token: Annotated[str, Header()]) -> None:
        auth_required = self.descriptor.auth
        if not auth_required:
            return
        if x_auth_token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        # TODO: Add auth logic here to validate the auth token
        if x_auth_token == "test123":
            return
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
