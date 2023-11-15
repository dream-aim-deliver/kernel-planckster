from abc import ABC, abstractmethod
from typing import Generic, Literal, Type

from pydantic import BaseModel, ConfigDict, validator
from lib.core.sdk.controller import BaseController, TBaseControllerParameters

from lib.core.sdk.presenter import Presentable
from lib.core.sdk.usecase_models import TBaseErrorResponse, TBaseRequest, TBaseResponse
from lib.core.sdk.viewmodel import TBaseViewModel


class BaseFeature(
    ABC,
    BaseModel,
    Generic[TBaseControllerParameters, TBaseRequest, TBaseResponse, TBaseErrorResponse, TBaseViewModel],
):
    name: str
    description: str
    version: str
    verb: Literal["GET", "POST", "PUT", "DELETE"]
    endpoint: str
    enabled: bool = True
    presenter: Presentable[TBaseResponse, TBaseErrorResponse, TBaseViewModel] | None = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        # ignored_types=(Presentable,),
    )

    @validator("endpoint")
    def endpoint_should_begin_with_slash(cls, v: str) -> str:
        if not v.startswith("/"):
            return f"/{v}"
        return v

    @abstractmethod
    def presenter_factory(self) -> Presentable[TBaseResponse, TBaseErrorResponse, TBaseViewModel]:
        raise NotImplementedError("You must implement the presenter_factory method in your feature")

    @abstractmethod
    def controller_factory(
        self,
    ) -> BaseController[TBaseControllerParameters, TBaseRequest, TBaseResponse, TBaseErrorResponse, TBaseViewModel]:
        raise NotImplementedError("You must implement the controller_factory method in your feature")

    def register(self) -> None:
        if not self.enabled:
            raise Exception(f"Cannot load {self}. Feature {self} is disabled")

    def execute(self, parameters: TBaseControllerParameters) -> TBaseViewModel | None:
        controller = self.controller_factory()
        if controller is None:
            raise Exception(f"Cannot execute {self.name} at {self.verb} {self.endpoint}. Controller is not defined")
        else:
            return controller.execute(parameters)
