import importlib
import os
from pathlib import Path
import signal
from typing import Any
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from lib.core.sdk.fastapi import FastAPIEndpoint
from lib.core.sdk.utils import get_all_modules
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.create_default_data_controller import (
    CreateDefaultDataController,
    CreateDefaultDataControllerParameters,
)
import lib.infrastructure.rest.endpoints as endpoints
from tools.app_startup_utils import (
    cleanup_handler,
    run_alembic_migrations,
    start_dependencies,
    stop_dependencies,
    wait_for_minio_to_be_responsive,
    wait_for_postgres_to_be_responsive,
)


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
    # Add CORS middleware
    default_origins = ["http://localhost", "http://localhost:3000", "http://localhost:8080"]
    allowed_origins = os.getenv("KP_ALLOWED_ORIGINS", "").split(",")
    final_origins = default_origins + [x.strip() for x in allowed_origins if x.strip() != ""]
    print(f"Allowed origins: {final_origins}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=final_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
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
    # Add CORS middleware
    default_origins = ["http://localhost", "http://localhost:3000", "http://localhost:8080"]
    allowed_origins = os.getenv("KP_ALLOWED_ORIGINS", "").split(",")
    final_origins = default_origins + [x.strip() for x in allowed_origins if x.strip() != ""]
    print(f"Allowed origins: {final_origins}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=final_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    host = app.container.config.fastapi.host()  # type: ignore
    port = app.container.config.fastapi.port()  # type: ignore
    uvicorn.run("lib.infrastructure.rest.main:create_app", host=host, port=port, reload=True)

    stop_dependencies(
        project_root_dir=Path(__file__).parent.parent.parent.parent,
        compose_rel_path=Path("docker-compose.yml"),
    )


def start() -> None:
    # check is provided RDBMS is reachable

    # check if RDBMS env vars are set
    rdbms_host = os.getenv("KP_RDBMS_HOST")
    rdbms_port = os.getenv("KP_RDBMS_PORT")
    rdbms_user = os.getenv("KP_RDBMS_USERNAME")
    rdbms_password = os.getenv("KP_RDBMS_PASSWORD")
    rdbms_db_name = os.getenv("KP_RDBMS_DBNAME")
    if not rdbms_host or not rdbms_port or not rdbms_user or not rdbms_password or not rdbms_db_name:
        raise Exception("RDBMS env vars are not set")

    wait_for_postgres_to_be_responsive(
        db_host=rdbms_host,
        db_port=int(rdbms_port),
        db_user=rdbms_user,
        db_password=rdbms_password,
        db_name=rdbms_db_name,
        max_retries=10,
        wait_seconds=5,
    )

    # Apply migrations
    project_root_dir = Path(__file__).parent.parent.parent.parent
    alemibc_ini_rel_path = Path("alembic.ini")
    alembic_ini_path = str(project_root_dir / alemibc_ini_rel_path)
    print(f"Alembic ini file: {alembic_ini_path}")
    alembic_scripts_path = str(project_root_dir / "alembic")
    run_alembic_migrations(
        alembic_ini_path=alembic_ini_path,
        alembic_scripts_path=alembic_scripts_path,
        db_host=rdbms_host,
        db_port=int(rdbms_port),
        db_user=rdbms_user,
        db_password=rdbms_password,
        db_name=rdbms_db_name,
    )

    # check if env vars for object store are set
    object_store_host = os.getenv("KP_OBJECT_STORE_HOST")
    object_store_port = os.getenv("KP_OBJECT_STORE_PORT")
    object_store_access_key = os.getenv("KP_OBJECT_STORE_ACCESS_KEY")
    object_store_secret_key = os.getenv("KP_OBJECT_STORE_SECRET_KEY")
    object_store_default_bucket = os.getenv("KP_OBJECT_STORE_BUCKET")
    object_store_secure = os.getenv("KP_OBJECT_STORE_SECURE", "true").lower() == "true"
    object_store_cert_check = os.getenv("KP_OBJECT_STORE_CERT_CHECK", "false").lower() == "true"

    if (
        not object_store_host
        or not object_store_port
        or not object_store_access_key
        or not object_store_secret_key
        or not object_store_default_bucket
    ):
        raise Exception("Object store env vars are not set")

    # check if provided object store is reachable
    wait_for_minio_to_be_responsive(
        host=object_store_host,
        port=int(object_store_port),
        access_key=object_store_access_key,
        secret_key=object_store_secret_key,
        secure=object_store_secure,
        cert_check=object_store_cert_check,
        default_bucket=object_store_default_bucket,
        max_retries=10,
        wait_seconds=5,
    )

    # TODO: check if provided Kafka is reachable

    app = create_app()

    # Add CORS middleware
    default_origins = ["http://localhost", "http://localhost:3000", "http://localhost:8080"]
    allowed_origins = os.getenv("KP_ALLOWED_ORIGINS", "").split(",")
    final_origins = default_origins + [x.strip() for x in allowed_origins if x.strip() != ""]
    print(f"Allowed origins: {final_origins}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=final_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    host = app.container.config.fastapi.host()  # type: ignore
    port = app.container.config.fastapi.port()  # type: ignore
    workers = app.container.config.fastapi.workers()  # type: ignore

    uvicorn.run(
        "lib.infrastructure.rest.main:create_app",
        host=host,
        port=port,
        proxy_headers=True,
        reload=False,
        workers=workers,
    )


if __name__ == "__main__":
    if os.getenv("KP_MODE") == "development":
        dev_server()
    elif os.getenv("KP_MODE") == "development_with_storage":
        dev_server_with_storage()
    else:
        # Production mode
        start()
