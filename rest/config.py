from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    host: str = "localhost"
    port: int = 8000
    model_config = SettingsConfigDict(env_file="../.env")
