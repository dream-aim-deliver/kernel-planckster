from abc import ABC, abstractmethod
from typing import Generic, Literal, Type

from pydantic import BaseModel, ConfigDict, validator
from lib.core.sdk.controller import BaseController, TBaseControllerParameters

from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase_models import TBaseErrorResponse, TBaseRequest, TBaseResponse
from lib.core.sdk.viewmodel import TBaseViewModel


class BaseFeatureDescriptor(
    ABC,
    BaseModel,
):
    name: str
    description: str
    version: str
    verb: Literal["GET", "POST", "PUT", "DELETE"]
    endpoint: str
    enabled: bool = True
    auth: bool = False
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    @validator("endpoint")
    def endpoint_should_begin_with_slash(cls, v: str) -> str:
        if not v.startswith("/"):
            return f"/{v}"
        return v
