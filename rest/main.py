from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any
from fastapi import APIRouter, FastAPI
import subprocess

import uvicorn
from lib.infrastructure.feature.demo_feature import DemoControllerParameters

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


@app.post("/")
def test(item: DemoControllerParameters) -> DemoControllerParameters:
    return item


def server() -> None:
    cmd = ["uvicorn", "main:app", "--reload", "--host", f"{settings.host}", "--port", f"{settings.port}"]
    subprocess.run(cmd)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
