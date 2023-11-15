from abc import ABC, abstractmethod
from typing import Any, Generic, Literal, Type, TypeVar
from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel, ConfigDict, Field, validator

from lib.core.sdk.presenter import Presentable
from lib.core.sdk.usecase_models import BaseResponse, TBaseErrorResponse, TBaseResponse
from lib.core.sdk.viewmodel import (
    BaseViewModel,
    TBaseViewModel,
    TBaseViewModel,
)

T = TypeVar("T", bound=BaseViewModel)


class FastAPIViewModelWrapper(BaseModel, Generic[T]):
    data: T | None = None


class FastAPIFeature(BaseModel, Generic[TBaseViewModel]):
    name: str
    description: str
    group: str
    verb: Literal["GET", "POST", "PUT", "DELETE"] = "GET"
    endpoint: str
    router: APIRouter | None = None
    presenter: Presentable[TBaseViewModel] | None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        # ignored_types=(Presentable,),
    )

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        group = data["group"]
        self.router: APIRouter = APIRouter(
            prefix=f"/{group}", tags=[group], responses={404: {"description": f"Not found"}}
        )
        self.register_endpoints(self.router)

    @validator("endpoint")
    def endpoint_should_begin_with_slash(cls, v: str) -> str:
        if not v.startswith("/"):
            return f"/{v}"
        return v

    @abstractmethod
    def endpoint_fn(self, request: Request, response: Response) -> TBaseViewModel:
        raise NotImplementedError("You must implement the endpoint_fn method in your feature")

    def register_endpoints(self, router: APIRouter) -> None:
        router.add_api_route(
            methods=[self.verb],
            tags=[self.group],
            path=f"{self.endpoint}",
            name=self.name,
            description=self.description,
            endpoint=self.endpoint_fn,
        )
