from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any
from fastapi import APIRouter, FastAPI
import subprocess

from rest.config import Settings, FEATURES


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


@asynccontextmanager
async def load_features(app: FastAPI) -> Any:
    for feature in FEATURES:
        router: APIRouter | None = feature.router
        if router is not None:
            app.router.include_router(router)
    yield None


app = FastAPI(lifespan=load_features)


def server() -> None:
    cmd = ["uvicorn", "main:app", "--reload", "--host", f"{settings.host}", "--port", f"{settings.port}"]
    subprocess.run(cmd)
