FROM python:3.10-bullseye

LABEL stage="production"

WORKDIR /opt/dadai/app
COPY . /opt/dadai/app

RUN pip install poetry
RUN python3 -m poetry install

CMD ["poetry", "run", "start"]
