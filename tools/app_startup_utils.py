from pathlib import Path
import subprocess
import time
import psycopg2
from alembic.config import Config
from alembic import command
from minio import Minio


def is_postgres_responsive(
    host: str,
    port: int,
    user: str,
    password: str,
    database: str,
) -> bool:
    try:
        conn = psycopg2.connect(host=host, database=database, port=port, user=user, password=password)
        return True
    except Exception as e:
        return False


def is_minio_responsive(
    host: str,
    port: int,
    access_key: str,
    secret_key: str,
    secure: bool,
    cert_check: bool,
    default_bucket: str,
) -> bool:
    try:
        print(f"Trying to connect to MinIO at {host}:{port}")
        minio = Minio(
            f"{host}:{port}",
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
            cert_check=cert_check,
        )
        if not minio.bucket_exists(default_bucket):
            minio.make_bucket(default_bucket)
        minio.remove_bucket(default_bucket)
        return True
    except Exception as e:
        print(f"Failed to connect to MinIO with error: {e}")
        return False


def wait_for_postgres_to_be_responsive(
    db_host: str,
    db_port: int,
    db_user: str,
    db_password: str,
    db_name: str,
    max_retries: int = 10,
    wait_seconds: int = 5,
) -> None:
    for i in range(max_retries):
        if is_postgres_responsive(host=db_host, port=db_port, user=db_user, password=db_password, database=db_name):
            return
        else:
            print(f"Postgres is not responsive yet, waiting {wait_seconds} seconds...")
            time.sleep(wait_seconds)
    raise Exception("Postgres is not responsive yet, aborting ...")


def wait_for_minio_to_be_responsive(
    host: str,
    port: int,
    access_key: str,
    secret_key: str,
    default_bucket: str,
    secure: bool = False,
    cert_check: bool = False,
    max_retries: int = 10,
    wait_seconds: int = 5,
) -> None:
    for i in range(max_retries):
        if is_minio_responsive(
            host=host,
            port=port,
            access_key=access_key,
            secret_key=secret_key,
            default_bucket=default_bucket,
            secure=secure,
            cert_check=cert_check,
        ):
            return
        else:
            print(f"MinIO is not responsive yet, waiting {wait_seconds} seconds...")
            time.sleep(wait_seconds)
    raise Exception("MinIO is not responsive yet, aborting ...")


def run_alembic_migrations(
    alembic_scripts_path: str,
    alembic_ini_path: str,
    db_host: str = "localhost",
    db_port: int = 5432,
    db_user: str = "postgres",
    db_password: str = "postgres",
    db_name: str = "kp-dev",
) -> None:
    alembic_cfg = Config(alembic_ini_path)

    alembic_cfg.set_main_option("script_location", alembic_scripts_path)

    alembic_cfg.set_main_option("sqlalchemy.url", f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

    try:
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        print(f"Failed to run alembic migrations with error: {e}")
        raise e


def cleanup_handler(signum, frame) -> None:  # type: ignore
    # This function will be called when a signal is received
    print(f"Received signal {signum}. Cleaning up...")
    # Add your cleanup logic here
    raise SystemExit(0)


def start_dependencies(
    project_root_dir: Path,
    compose_rel_path: Path = Path("docker-compose.yml"),
    alemibc_ini_rel_path: Path = Path("alembic.ini"),
    pg_host: str = "localhost",
    pg_port: int = 5432,
    pg_user: str = "postgres",
    pg_password: str = "postgres",
    pg_db: str = "kp-dev",
    enable_storage: bool = False,
    object_store_host: str = "localhost",
    object_store_port: int = 9001,
    object_store_access_key: str = "minio",
    object_store_secret_key: str = "minio123",
    object_store_secure: bool = False,
    object_store_cert_check: bool = False,
    object_store_default_bucket: str = "default",
) -> None:
    print("Starting Docker Compose service...")
    compose_file = str(project_root_dir / compose_rel_path)
    print(f"Compose file: {compose_file}")
    alembic_ini_path = str(project_root_dir / alemibc_ini_rel_path)
    print(f"Alembic ini file: {alembic_ini_path}")
    alembic_scripts_path = str(project_root_dir / "alembic")
    docker_compose_cmd = ["docker", "compose", "--profile", "dev", "-f", compose_file, "up", "-d"]
    if enable_storage:
        docker_compose_cmd = ["docker", "compose", "--profile", "storage", "-f", compose_file, "up", "-d"]
    # Start Docker Compose service
    process = subprocess.Popen(
        docker_compose_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = process.communicate()

    # Print the output of the Docker Compose down command
    print("Docker Compose Up Output:")
    print(out)
    print("Docker Compose Up Error:")
    print(err)

    # Wait for the service to be ready (you might need to adjust the delay)
    wait_for_postgres_to_be_responsive(
        db_host=pg_host,
        db_port=pg_port,
        db_user=pg_user,
        db_password=pg_password,
        db_name=pg_db,
        max_retries=10,
        wait_seconds=5,
    )

    # Wait for MinIO to be ready
    if enable_storage:
        wait_for_minio_to_be_responsive(
            host=object_store_host,
            port=object_store_port,
            access_key=object_store_access_key,
            secret_key=object_store_secret_key,
            default_bucket=object_store_default_bucket,
            secure=object_store_secure,
            cert_check=object_store_cert_check,
            max_retries=10,
            wait_seconds=5,
        )
    # Run Alembic migrations
    run_alembic_migrations(
        alembic_ini_path=alembic_ini_path,
        alembic_scripts_path=alembic_scripts_path,
        db_host=pg_host,
        db_port=pg_port,
        db_user=pg_user,
        db_password=pg_password,
        db_name=pg_db,
    )

    if enable_storage:
        # intialize the object store
        pass


def stop_dependencies(
    project_root_dir: Path,
    compose_rel_path: Path = Path("docker-compose.yml"),
) -> None:
    print("Stopping Docker Compose service...")
    compose_file = str(project_root_dir / compose_rel_path)
    print(f"Compose file: {compose_file}")
    # Stop Docker Compose service
    process = subprocess.Popen(
        ["docker", "compose", "--profile", "*", "-f", compose_file, "down", "-v", "--remove-orphans"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = process.communicate()

    # Print the output of the Docker Compose down command
    print("Docker Compose Down Output:")
    print(out)
    print("Docker Compose Down Error:")
    print(err)
