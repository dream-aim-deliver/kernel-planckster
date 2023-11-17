from contextlib import contextmanager
import subprocess
import time

import psycopg2
from alembic.config import Config
from alembic import command


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


def wait_for_postgres_to_be_responsive(
    host: str,
    port: int,
    user: str,
    password: str,
    database: str,
    max_retries: int = 10,
    wait_seconds: int = 5,
) -> None:
    for i in range(max_retries):
        if is_postgres_responsive(host=host, port=port, user=user, password=password, database=database):
            return
        else:
            print(f"Postgres is not responsive yet, waiting {wait_seconds} seconds...")
            time.sleep(wait_seconds)
    raise Exception("Postgres is not responsive yet, aborting tests...")


@contextmanager
def docker_compose_context(  # type: ignore
    compose_file,
    pg_host="localhost",
    pg_port=5432,
    pg_user="postgres",
    pg_password="postgres",
    pg_db="kp-dev",
):
    try:
        # Start Docker Compose service
        process = subprocess.Popen(
            ["docker-compose", "-f", compose_file, "up", "-d"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Wait for the service to be ready (you might need to adjust the delay)
        wait_for_postgres_to_be_responsive(
            host=pg_host,
            port=pg_port,
            user=pg_user,
            password=pg_password,
            database=pg_db,
            max_retries=10,
            wait_seconds=5,
        )

        yield

    finally:
        # Clean up: Stop and remove Docker Compose service
        process = subprocess.Popen(
            ["docker-compose", "-f", compose_file, "down", "-v", "--remove-orphans"],
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


def run_alembic_migrations(
    alembic_ini_path: str,
    db_host: str = "localhost",
    db_port: int = 5432,
    db_user: str = "postgres",
    db_password: str = "postgres",
    db_name: str = "kp-dev",
) -> None:
    alembic_ini_path = os.path.join(str(request.config.rootdir), "alembic.ini")  # type: ignore
    alembic_cfg = Config(alembic_ini_path)

    alembic_scripts_path = os.path.join(str(request.config.rootdir), "alembic")  # type: ignore
    alembic_cfg.set_main_option("script_location", alembic_scripts_path)

    alembic_cfg.set_main_option("sqlalchemy.url", f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

    try:
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        print(f"Failed to run alembic migrations with error: {e}")
        raise e
