from typing import Dict
from pydantic import BaseModel, ConfigDict, field_validator
from dependency_injector import containers, providers


class BaseFeatureDescriptor(
    BaseModel,
):
    name: str
    description: str
    # verb: Literal["GET", "POST", "PUT", "DELETE"]
    # endpoint: str
    enabled: bool = True
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    # @field_validator("endpoint")
    # def endpoint_should_begin_with_slash(cls, v: str) -> str:
    #     if not v.startswith("/"):
    #         return f"/{v}"
    #     return v


class BaseFeatureSetDescriptor(
    BaseModel,
):
    name: str
    description: str
    version: str
    collection: str
    enabled: bool = True
    auth: bool = False
    features: Dict[str, BaseFeatureDescriptor]
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


class BaseFeatureSetContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    # add wiring config to FastAPI  router module
    feature_set_descriptor = providers.Factory(
        BaseFeatureSetDescriptor,
        name=config.name,
        description=config.description,
        version=config.version,
        collection=config.tag,
        enabled=config.enabled,
        auth=config.auth,
        features=config.features,
    )
