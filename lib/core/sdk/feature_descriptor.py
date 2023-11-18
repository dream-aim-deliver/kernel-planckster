from abc import ABC, abstractmethod
from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator


class BaseFeatureDescriptor(
    BaseModel,
):
    name: str
    description: str
    version: str
    tags: list[str] = []
    enabled: bool = True
    auth: bool = False
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
