# Starter template for a clean architecture python project

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Installation


## Features


## Development

### Setup

```bash
# AT THE ROOT OF THE PROJECT

# OPTIONAL: create a virtual environment and activate it
python3 -m venv .venv
source .venv/bin/activate

# Install poetry
pip install poetry

# Install dependencies
poetry install

# Setup pre-commit
pre-commit install
pre-commit run --all-files

# Create a .env file
cp .env.example .env

# Set up environment variables for pytest in pyproject.toml as needed
```


### Autogenerate Alembic Migrations

Using docker containers to spin up an SQL database, you can autogenerate migrations with Alembic:

```bash
cd tests
docker compose up -d
cd ../
alembic upgrade head
alembic revision --autogenerate -m "migration message"
alembic upgrade head
alembic downgrade base
alembic upgrade head
cd tests
docker compose down
```

Make sure to fix any errors given by the alembic commands above before executing the next one and commiting the changes.


### Accessing the database

You can access `<DB explorer>` at `http://localhost:<PORT>` to check the database. The credentials are:
```
System:
Server:
Username:
Password:
Database:
```

### Pull Requests

Before submitting a pull request, please:

1. Run pytest, at the root of the project, and fix all the errors:
```bash
poetry run pytest -s
```

2. Run mypy, at the root of the project, and fix all type errors:
```bash
poetry run mypy .
```

3. Run black, at the root of the project
```bash
poetry run black .
```


