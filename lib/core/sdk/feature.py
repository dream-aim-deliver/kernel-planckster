from abc import ABC, abstractmethod
from typing import Generic, Literal, Type

from pydantic import BaseModel, ConfigDict, validator

from lib.core.sdk.presenter import Presentable
from lib.core.sdk.viewmodel import TBaseViewModel


class BaseFeature(
    ABC,
    BaseModel,
    Generic[TBaseViewModel],
):
    name: str
    description: str
    version: str
    verb: Literal["GET", "POST", "PUT", "DELETE"]
    endpoint: str
    auth_required: bool = False
    enabled: bool = True
    presenter: Presentable[TBaseViewModel] | None = None

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
    def presenter_factory(self) -> Presentable[TBaseViewModel]:
        raise NotImplementedError("You must implement the presenter_factory method in your feature")

    def register(self) -> None:
        if not self.enabled:
            raise Exception(f"Cannot load {self}. Feature {self} is disabled")
