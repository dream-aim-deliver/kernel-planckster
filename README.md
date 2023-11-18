# Kernel Planckster [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This repository contains the core management system for Max Planck Institute Data Systems Group's Satellite Data Augmentation Project. It is being developed by DAD (Dream, Aim, Deliver) as part of the collaboration with the Max Planck Institute.

## Development

### Forks
Please fork this repository to your own GitHub account and clone it to your local machine.
Please avoid pushing to this repository directory directly, either to the main branch or to any other branch.

```bash
gh repo clone <your-username>/kernel-planckster

git remote add upstream https://github.com/dream-aim-deliver/kernel-planckster.git
```
Then head over to 
```
https://github.com/<your_username>/kernel-planckster/settings/actions
```

and enable GitHub Actions for your fork by selecting the `Allow all actions and reusable workflows` option.


### Database Models

![Database Models](docs/kernel-planckster-db-models.png)


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

# Set up environment variables for pytest in pyproject.toml as needed, but the defaults should work
```


### Autogenerate Alembic Migrations

Using docker containers to spin up an SQL database, you can autogenerate migrations with Alembic. From the root of the project, do:

```bash
docker compose up -d
alembic upgrade head
alembic revision --autogenerate -m "migration message"
alembic upgrade head
alembic downgrade base
alembic upgrade head
docker compose down
```

Make sure to fix any errors given by the alembic commands above before executing the next one and commiting the changes.


### Accessing the server and database

For development, the environment variable `KP_MODE` has to be set to `development`. This is the default value used by the `docker-compose.yml` and `launch.json` files.

In development mode, postgres, fastapi and adminer are all running in docker containers. These containers will be started automatically when you start `FastAPI` launch configuration in VSCode or when you run the `dev` script in the root of the project, as shown below:

```bash
poetry run dev
```

The containers will be removed when you stop the `dev` script or stop the `FastAPI` launch configuration in VSCode.

| Service    | Host/Port             | Mode        |
| ---------- | --------------------- | ----------- |
| FastAPI    | http://localhost:8000 | development |
| Postgres   | 0.0.0.0:5432          | development |
| Adminer UI | http://localhost:8080 | development |


In development mode, you can access `Adminer interface` at `http://localhost:8080` to check the database. The credentials are:

```
System: PostgreSQL
Server: db
Username: postgres
Password: postgres
Database: kp-db
```

## Testing
You run tests on the command line with
```bash
poetry run pytest -s
``` 

Or in the [VSCode test explorer UI](https://marketplace.visualstudio.com/items?itemName=hbenl.vscode-test-explorer).

In test mode, postgres, fastapi and adminer are all running in docker container and will be automatically removed once the tests are finished. 

**DANGLING CONTAINER WARNING**: If you are debugging tests in VSCode and notice that your test is failing, which triggers a breakpoint, then DO NOT STOP the debugger. Just press `F5` and let the tests finish. The containers will be removed automatically once the tests are finished. Otherwise, you will end up with dangling test containers that will have to be removed manually. To remove these containers manually

```bash
cd tests
docker compose down
```

In testing mode, you can access the services as follows:
| Service    | Host/Port             | Mode |
| ---------- | --------------------- | ---- |
| FastAPI    | http://localhost:8005 | test |
| Postgres   | 0.0.0.0:5435          | test |
| Adminer UI | http://localhost:8085 | test |


In test mode, you can access `Adminer interface` at `http://localhost:8085` to check the database. The credentials are:

```
System: PostgreSQL
Server: db
Username: postgres
Password: postgres
Database: kp-db
```


### Running the production server (FastAPI/Socket.IO)

You can start the FastAPI production server with:

```bash
 cd lib/infrastructure/rest
 export KP_MODE=production
 export KP_DB_URL=postgresql://postgres:postgres@localhost:5432/kp-db
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

If you add a [github-recognised keyword](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) in the pull request name or in the pull request description, then the associated issue can be closed automatically once the pull request is merged, e.g.:


```bash
<component>: <change_message> Fix #<issue number>
```
