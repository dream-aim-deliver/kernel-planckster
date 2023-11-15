from typing import Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from lib.core.sdk.caps_fastapi import FastAPIFeature

from lib.infrastructure.feature.demo_feature import DemoFeature


class Settings(BaseSettings):
    host: str = "localhost"
    port: int = 8000
    model_config = SettingsConfigDict(env_file="../.env")


FEATURES: list[FastAPIFeature[Any]] = [DemoFeature()]
