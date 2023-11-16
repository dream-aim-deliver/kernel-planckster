from typing import Any, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import Sequence
from lib.core.sdk.caps_fastapi import FastAPIFeature


class Settings(BaseSettings):
    host: str = "localhost"
    port: int = 8000
    model_config = SettingsConfigDict(env_file="../.env")
