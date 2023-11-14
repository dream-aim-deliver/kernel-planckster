from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any, Generic
from fastapi import APIRouter, FastAPI
import subprocess

from fastapi.responses import JSONResponse
from lib.core.sdk.caps_fastapi import FastAPIFeature
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseResponse
from lib.core.sdk.viewmodel import BaseViewModel

from rest.config import Settings


class DemoFeature(FastAPIFeature[BaseResponse, BaseErrorResponse, BaseViewModel]):
    pass


demoFeature = DemoFeature(
    name="Demo",
    description="Demo Feature",
    group="demo",
    verb="GET",
    endpoint="/endpoint",
)


@asynccontextmanager
async def load_features(app: FastAPI) -> Any:
    router: APIRouter | None = demoFeature.router
    if router is not None:
        app.router.include_router(router)
    yield None


app = FastAPI(lifespan=load_features)


@lru_cache()
def get_settings() -> Settings:
    return Settings()


@app.get("/")
def read_root() -> JSONResponse:
    response = JSONResponse(status_code=404, content="Not Found")
    return response


def server() -> None:
    settings = get_settings()
    cmd = ["uvicorn", "main:app", "--reload", "--host", f"{settings.host}", "--port", f"{settings.port}"]
    subprocess.run(cmd)
