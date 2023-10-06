# Kernel Planckster [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This repository contains the core management system for Max Planck Institute Data Systems Group's Satellite Data Augmentation Project. It is being developed by DAD (Dream, Aim, Deliver) as part of the collaboration with the Max Planck Institute.

## Development

### Forks
Please fork this repository to your own GitHub account and clone it to your local machine.
Please avoid pushing to this repository directory directly, either to the main branch or to any other branch.

```bash
gh repo clone <your-username>/kernel-planckster
```


### Setup

```bash
# AT THE ROOT OF THE PROJECT

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

You can access `Adminer interface` at `http://localhost:8080` to check the database. The credentials are:
```
System: PostgreSQL
Server: kp-test
Username: postgres
Password: postgres
Database: kp-db
```

### Running the development server (FastAPI/Socket.IO)

You can start the FastAPI development server with:

```bash
 poetry run dev
```

## Contributing

We use VSCode as our IDE. If you use VSCode, please install the recommended extensions.

### Issues
Please use [Issues](https://github.com/dream-aim-deliver/kernel-planckster/issues) to report any bugs or feature requests.


Once you have been assigned an issue, please create a branch with the following naming convention:
```
feature-<issue number>-<short description>
```

We recommend using the provided `create-feature-branch` utility to create a branch with the correct name. 
This script will also pull the latest changes from the remote repository and create the new branch for you to work in.


```bash
./tools/create-feature-branch <issue number> <short description>
```
### Commits
Commit your change. The commit command must include a specific message format:

```
git commit -m "<component>: <change_message> #<issue number>"
```

Valid component names are listed in the [label](https://github.com/dream-aim-deliver/kernel-planckster/labels) list and are usually specified on the issue of the change.

Add additional explanations to the body of the commit, such as motivation for certain decisions and background information. Here are some general rules: https://cbea.ms/git-commit/.

If you add a [github-recognised keyword](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) then the associated issue can be closed automatically once the pull request is merged, e.g.:

```bash
<component>: <change_message> Fix #<issue number>
```

Using multiple commits is allowed as long as they achieve an independent, well-defined, change and are well-described. Otherwise multiple commits should be squashed.

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

Push the commit to your forked repository and create the pull request. Try to keep the Pull Request simple, it should achieve the single objective described in the issue. Multiple enhancements/fixes should be split into multiple Pull Requests.

Watch the pull request for comments and reviews. For any pull requests update, please try to squash/amend your commits to avoid “in-between” commits.