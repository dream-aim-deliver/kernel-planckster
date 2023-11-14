from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any
from fastapi import APIRouter, FastAPI, Request, Response
import subprocess

from fastapi.responses import JSONResponse
from lib.core.sdk.caps_fastapi import FastAPIFeature

from rest.config import Settings

demoFeature = FastAPIFeature(
    name="Demo",
    description="Demo Feature",
    base="demo",
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
