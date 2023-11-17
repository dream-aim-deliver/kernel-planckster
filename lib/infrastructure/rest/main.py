from contextlib import contextmanager
import importlib
from pathlib import Path
import time
from typing import Any
from fastapi import APIRouter, FastAPI
import subprocess

import uvicorn
from lib.core.sdk.fastapi import FastAPIFeature
from lib.core.sdk.utils import get_all_modules
from lib.infrastructure.config.containers import ApplicationContainer
import lib.infrastructure.rest.endpoints as endpoints


def create_app(app_container: ApplicationContainer | None = None) -> tuple[FastAPI, ApplicationContainer]:
    app = FastAPI()
    if app_container is None:
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


if __name__ == "__main__":
    # if(app_container.config.mode == "development"):

    host = app_container.config.fastapi.host()
    port = app_container.config.fastapi.port()
    uvicorn.run(app, host=host, port=port)
