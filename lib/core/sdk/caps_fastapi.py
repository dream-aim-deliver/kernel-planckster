from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Literal, Type, TypeVar
from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel, ConfigDict, Field, model_validator, validator
from lib.core.sdk.feature import BaseFeature

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


class FastAPIFeature(BaseFeature[TBaseViewModel], Generic[TBaseViewModel]):
    name: str
    description: str
    group: str
    verb: Literal["GET", "POST", "PUT", "DELETE"] = "GET"
    endpoint: str
    responses: Dict[int | str, dict[str, Any]] | None = None
    router: APIRouter | None = None
    # presenter: Presentable[TBaseViewModel] | None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        # ignored_types=(Presentable,),
    )

    @model_validator(mode="after")  # type: ignore
    def populate_arbitrary_fields(cls, instance: "FastAPIFeature[BaseViewModel]") -> "FastAPIFeature[BaseViewModel]":
        group = instance.group
        instance.router = APIRouter(prefix=f"/{group}", tags=[group])
        instance.register_endpoints(instance.router)

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
            responses=self.responses,
        )
