from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  # type: ignore
    host: str
    port: int
    model_config = SettingsConfigDict(env_file="../.env")
