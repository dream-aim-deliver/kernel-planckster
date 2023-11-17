from abc import ABC, abstractmethod
from typing import Literal

from pydantic import BaseModel, ConfigDict, validator


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
