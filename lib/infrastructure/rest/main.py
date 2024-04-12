import importlib
import os
from pathlib import Path
import signal
from typing import Any
from fastapi import APIRouter, FastAPI

import uvicorn
from lib.core.sdk.fastapi import FastAPIEndpoint
from lib.core.sdk.utils import get_all_modules
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.create_default_data_controller import (
    CreateDefaultDataController,
    CreateDefaultDataControllerParameters,
)
import lib.infrastructure.rest.endpoints as endpoints
from tools.app_startup_utils import cleanup_handler, start_dependencies, stop_dependencies


def create_app() -> FastAPI:
    app = FastAPI()
    app_container = ApplicationContainer()
    app_container.config.from_yaml("../../../config.yaml")
    app.container = app_container  # type: ignore

    create_default_data_controller: CreateDefaultDataController = (
        app_container.create_default_data_feature().controller()
    )
    default_parameters: CreateDefaultDataControllerParameters = CreateDefaultDataControllerParameters(
        client_sub=None, llm_name=None
    )
    create_default_data_controller.execute(default_parameters)
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
        app.get(
            "/ping",
            name="health",
            tags=["Health Check"],
            summary="Health Check",
            description="Checks if Kernel Planchester is alive",
            response_model=Any,
        )(lambda: {"pong"})
    return app


def dev_server() -> None:
    signal.signal(signal.SIGTERM, cleanup_handler)
    signal.signal(signal.SIGINT, cleanup_handler)

    start_dependencies(
        project_root_dir=Path(__file__).parent.parent.parent.parent,
        compose_rel_path=Path("docker-compose.yml"),
        alemibc_ini_rel_path=Path("alembic.ini"),
        pg_host=os.getenv("KP_RDBMS_HOST", "0.0.0.0"),
        pg_port=int(os.getenv("KP_RDBMS_PORT", "5432")),
        pg_user=os.getenv("KP_RDBMS_USERNAME", "postgres"),
        pg_password=os.getenv("KP_RDBMS_PASSWORD", "postgres"),
        pg_db=os.getenv("KP_RDBMS_DBNAME", "kp-db"),
    )
    app = create_app()
    host = app.container.config.fastapi.host()  # type: ignore
    port = app.container.config.fastapi.port()  # type: ignore
    uvicorn.run("lib.infrastructure.rest.main:create_app", host=host, port=port, reload=True)

    stop_dependencies(
        project_root_dir=Path(__file__).parent.parent.parent.parent,
        compose_rel_path=Path("docker-compose.yml"),
    )


def dev_server_with_storage() -> None:
    signal.signal(signal.SIGTERM, cleanup_handler)
    signal.signal(signal.SIGINT, cleanup_handler)

    start_dependencies(
        project_root_dir=Path(__file__).parent.parent.parent.parent,
        compose_rel_path=Path("docker-compose.yml"),
        alemibc_ini_rel_path=Path("alembic.ini"),
        pg_host=os.getenv("KP_RDBMS_HOST", "0.0.0.0"),
        pg_port=int(os.getenv("KP_RDBMS_PORT", "5432")),
        pg_user=os.getenv("KP_RDBMS_USERNAME", "postgres"),
        pg_password=os.getenv("KP_RDBMS_PASSWORD", "postgres"),
        pg_db=os.getenv("KP_RDBMS_DBNAME", "kp-db"),
        enable_storage=True,
        object_store_host=os.getenv("KP_OBJECT_STORE_HOST", "localhost"),
        object_store_port=int(os.getenv("KP_OBJECT_STORE_PORT", "9001")),
        object_store_access_key=os.getenv("KP_OBJECT_STORE_ACCESS_KEY", "minio"),
        object_store_secret_key=os.getenv("KP_OBJECT_STORE_SECRET_KEY", "minio123"),
        object_store_default_bucket=os.getenv("KP_OBJECT_STORE_DEFAULT_BUCKET", "default"),
    )
    app = create_app()
    host = app.container.config.fastapi.host()  # type: ignore
    port = app.container.config.fastapi.port()  # type: ignore
    uvicorn.run("lib.infrastructure.rest.main:create_app", host=host, port=port, reload=True)

    stop_dependencies(
        project_root_dir=Path(__file__).parent.parent.parent.parent,
        compose_rel_path=Path("docker-compose.yml"),
    )


def start() -> None:
    app = create_app()
    host = app.container.config.fastapi.host()  # type: ignore
    port = app.container.config.fastapi.port()  # type: ignore
    uvicorn.run("lib.infrastructure.rest.main:create_app", host=host, port=port, proxy_headers=True, reload=False)


if __name__ == "__main__":
    if os.getenv("KP_MODE") == "development":
        dev_server()
    elif os.getenv("KP_MODE") == "development_with_storage":
        dev_server_with_storage()
    else:
        # Production mode
        start()
