import importlib
from pathlib import Path
from typing import Any
from fastapi import APIRouter, FastAPI
import subprocess

import uvicorn
from lib.core.sdk.fastapi import FastAPIFeature
from lib.core.sdk.utils import get_all_modules
from lib.infrastructure.config.containers import ApplicationContainer
import lib.infrastructure.rest.endpoints as endpoints


app_container = ApplicationContainer()


def create_app() -> tuple[FastAPI, ApplicationContainer]:
    app = FastAPI()
    app_container = ApplicationContainer()
    app_container.config.from_yaml("../../../config.yaml")
    app.container = app_container  # type: ignore

    fastapi_endpoints = get_all_modules(package=endpoints, relative_package_dir=Path(__file__).parent / "endpoints")

    for fastapi_endpoint in fastapi_endpoints:
        module = importlib.import_module(fastapi_endpoint)

        fastapi_feature_class = next(
            (
                obj
                for name, obj in module.__dict__.items()
                if isinstance(obj, type) and "FastAPIFeature" in obj.__name__ and obj != FastAPIFeature
            ),
            None,
        )
        if fastapi_feature_class is None:
            continue
        else:
            fastapi_feature = fastapi_feature_class()
            router: APIRouter | None = fastapi_feature.load()
            if router is not None:
                app.include_router(fastapi_feature.router)
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
