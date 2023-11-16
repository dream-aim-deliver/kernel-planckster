from typing import Literal
from pydantic import BaseModel, ConfigDict, field_validator


class BaseFeatureDescriptor(
    BaseModel,
):
    name: str
    description: str
    version: str
    collection: str
    verb: Literal["GET", "POST", "PUT", "DELETE"]
    endpoint: str
    enabled: bool = True
    auth: bool = False
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    @field_validator("endpoint")
    def endpoint_should_begin_with_slash(cls, v: str) -> str:
        if not v.startswith("/"):
            return f"/{v}"
        return v


class BaseFeatureSetDescriptor(
    BaseModel,
):
    name: str
    description: str
    version: str
    collection: str
    enabled: bool = True
    auth: bool = False
    features: list[BaseFeatureDescriptor]
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
