import importlib
import os
from pathlib import Path
import signal
from typing import Any
from fastapi import APIRouter, FastAPI
import subprocess

import uvicorn
from lib.core.sdk.fastapi import FastAPIEndpoint
from lib.core.sdk.utils import get_all_modules
from lib.infrastructure.config.containers import ApplicationContainer
import lib.infrastructure.rest.endpoints as endpoints
from tools.app_startup_utils import cleanup_handler, docker_compose_context, start_depdendencies, stop_dependencies


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
                if isinstance(obj, type) and "FastAPIFeature" in obj.__name__ and obj != FastAPIEndpoint
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


def load_app() -> FastAPI:
    app, _ = create_app()
    return app


def hot_reload() -> None:
    signal.signal(signal.SIGTERM, cleanup_handler)
    signal.signal(signal.SIGINT, cleanup_handler)
    start_depdendencies(
        project_root_dir=Path(__file__).parent.parent.parent.parent,
        compose_rel_path=Path("docker-compose.yml"),
        alemibc_ini_rel_path=Path("alembic.ini"),
        pg_host=os.getenv("KP_PG_HOST", "0.0.0.0"),
        pg_port=int(os.getenv("KP_PG_PORT", "5432")),
        pg_user=os.getenv("KP_PG_USER", "postgres"),
        pg_password=os.getenv("KP_PG_PASSWORD", "postgres"),
        pg_db=os.getenv("KP_PG_DB", "kp-db"),
    )
    app, app_container = create_app()
    host = app_container.config.fastapi.host()
    port = app_container.config.fastapi.port()
    uvicorn.run("lib.infrastructure.rest.main:load_app", host=host, port=port, reload=True)

    stop_dependencies(
        project_root_dir=Path(__file__).parent.parent.parent.parent,
        compose_rel_path=Path("docker-compose.yml"),
    )


def dev_server() -> None:
    with docker_compose_context(
        project_root_dir=Path(__file__).parent.parent.parent.parent,
        compose_rel_path=Path("docker-compose.yml"),
        alemibc_ini_rel_path=Path("alembic.ini"),
        pg_host=os.getenv("KP_PG_HOST", "0.0.0.0"),
        pg_port=int(os.getenv("KP_PG_PORT", "5432")),
        pg_user=os.getenv("KP_PG_USER", "postgres"),
        pg_password=os.getenv("KP_PG_PASSWORD", "postgres"),
        pg_db=os.getenv("KP_PG_DB", "kp-db"),
    ):
        app, app_container = create_app()
        host = app_container.config.fastapi.host()
        port = app_container.config.fastapi.port()
        uvicorn.run("main:serve", host=host, port=port, reload=True)


if __name__ == "__main__":
    if os.getenv("KP_MODE") == "development":
        hot_reload()
    else:
        app, app_container = create_app()
        host = app_container.config.fastapi.host()
        port = app_container.config.fastapi.port()
        uvicorn.run(app, host=host, port=port)
