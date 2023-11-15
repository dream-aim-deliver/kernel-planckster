from abc import ABC, abstractmethod
from typing import Any, Generic, Literal, Type, TypeVar
from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel, ConfigDict, Field, validator

from lib.core.sdk.presenter import Presentable
from lib.core.sdk.usecase_models import BaseResponse, TBaseErrorResponse, TBaseResponse
from lib.core.sdk.viewmodel import (
    BaseErrorViewModel,
    BaseSuccessViewModel,
    TBaseErrorViewModel,
    TBaseSuccessViewModel,
    TBaseViewModel,
)

T = TypeVar("T", bound=BaseSuccessViewModel)


class FastAPIViewModelWrapper(BaseModel, Generic[T]):
    data: T | None = None


class FastAPIFeature(BaseModel, Generic[TBaseSuccessViewModel]):
    name: str
    description: str
    group: str
    verb: Literal["GET", "POST", "PUT", "DELETE"] = "GET"
    endpoint: str
    router: APIRouter | None = None
    presenter: Presentable[TBaseSuccessViewModel] | None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        # ignored_types=(Presentable,),
    )

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        group = data["group"]
        name = data["name"]
        self.router: APIRouter = APIRouter(
            prefix=f"/{group}", tags=[group], responses={404: {"description": f"Not found {name}"}}
        )
        self.register_endpoints(self.router)

    @validator("endpoint")
    def endpoint_should_begin_with_slash(cls, v: str) -> str:
        if not v.startswith("/"):
            return f"/{v}"
        return v

    def register_endpoints(self, router: APIRouter) -> None:
        # @router.get(f"{self.endpoint}")
        def register_endpoint(request: Request) -> FastAPIViewModelWrapper[TBaseSuccessViewModel]:
            presenter = self.presenter
            if presenter is None:
                raise HTTPException(status_code=500, detail="Presenter is not defined")
            else:
                data = presenter.present_success(response=BaseResponse(status=True, result="Hello World!"))
                return FastAPIViewModelWrapper(data=data)

        router.add_api_route(
            methods=[self.verb],
            tags=[self.group],
            path=f"{self.endpoint}",
            name=self.name,
            description=self.description,
            endpoint=register_endpoint,
        )
