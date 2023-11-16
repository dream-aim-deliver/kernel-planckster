from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any
from fastapi import APIRouter, FastAPI
import subprocess

import uvicorn
from lib.infrastructure.config.containers import Container
from rest.config import Settings
from lib.infrastructure.routers.demo_router import router


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
    app = FastAPI()
    app_container = Container()
    app.container = app_container  # type: ignore
    feature_sets = app_container.config.feature_sets()
    for feature_set_name, feature_set in feature_sets.items():
        for feature_name, feature in feature_set["features"].items():
            print(feature)
            # router: APIRouter | None = feature.router
            # if router is not None:
            # app.router.include_router(router)
    demo_router: APIRouter = router  # type: ignore
    app.router.include_router(demo_router)
    return app


app = create_app()


def server() -> None:
    cmd = ["uvicorn", "main:app", "--reload", "--host", f"{settings.host}", "--port", f"{settings.port}"]
    subprocess.run(cmd)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
