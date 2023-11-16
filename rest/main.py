from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any
from fastapi import APIRouter, FastAPI
import subprocess

import uvicorn
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.config.demo_feature import DemoFastAPIFeature
from lib.infrastructure.controller.demo_controller import DemoControllerParameters
from rest.config import Settings


# TODO: move settings to config.yaml
@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


# @asynccontextmanager
# async def load_features(app: FastAPI) -> Any:
#     for feature in FEATURES:
#         router: APIRouter | None = feature.router
#         if router is not None:
#             app.router.include_router(router)
#     yield None


# app = FastAPI(lifespan=load_features)


def create_app() -> FastAPI:
    container = ApplicationContainer()
    app = FastAPI()
    # TODO: might be optional actually, remove this line below and test
    app.container = container  # type: ignore
    demo_feature = DemoFastAPIFeature()
    router: APIRouter | None = demo_feature.load()
    if router is not None:
        app.include_router(demo_feature.router)
    return app


app = create_app()


@app.post("/")
def test(item: DemoControllerParameters) -> DemoControllerParameters:
    return item


def server() -> None:
    cmd = ["uvicorn", "main:app", "--reload", "--host", f"{settings.host}", "--port", f"{settings.port}"]
    subprocess.run(cmd)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
