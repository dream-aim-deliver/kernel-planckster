from typing import Any
from fastapi import APIRouter, FastAPI
import subprocess

import uvicorn
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.config.demo_feature import DemoFastAPIFeature


app_container = ApplicationContainer()


def create_app() -> tuple[FastAPI, ApplicationContainer]:
    app = FastAPI()
    app_container = ApplicationContainer()
    app_container.config.from_yaml("../config.yaml")
    app.container = app_container  # type: ignore
    demo_feature = DemoFastAPIFeature()
    router: APIRouter | None = demo_feature.load()
    if router is not None:
        app.include_router(demo_feature.router)
    return app, app_container


app, app_container = create_app()


def server() -> None:
    host = app_container.config.fastapi.host()
    port = app_container.config.fastapi.port()
    cmd = ["uvicorn", "main:app", "--reload", "--host", f"{host}", "--port", f"{port}"]
    subprocess.run(cmd)


if __name__ == "__main__":
    host = app_container.config.fastapi.host()
    port = app_container.config.fastapi.port()
    uvicorn.run(app, host=host, port=port)
