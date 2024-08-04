# Deployment Overview

This guide describes how to start a production deployment of the application using Docker.
For running the application in a Kubernetes cluster, please follow the deployment guide in [Kubesat Planckster](https://github.com/dream-aim-deliver/kubesat-planckster), which contains the necessary Kubernetes manifests.

## Prerequisites

- Docker

## Build the Docker image

To build the Docker image, run the following command:

```bash
docker build --rm -t maany/kernel-planckster .
```

## Bring up the dependencies
```
docker compose -f docker-compose.yml --profile storage up -d
```

## Run the Docker container

To run the Docker container, run the following command:

```bash
docker run -d --name kernel-planckster \
    -p 8000:8000 \
    -e KP_FASTAPI_HOST=localhost \
    -e KP_FASTAPI_PORT=8000 \
    -e KP_RDBMS_HOST=db \
    -e KP_RDBMS_PORT=5432 \
    -e KP_RDBMS_USERNAME=postgres \
    -e KP_RDBMS_PASSWORD=postgres \
    -e KP_RDBMS_DBNAME=kp-db \
    -e KP_OBJECT_STORE_HOST=minio \
    -e KP_OBJECT_STORE_PORT=9001 \
    -e KP_OBJECT_STORE_ACCESS_KEY=minio \
    -e KP_OBJECT_STORE_SECRET_KEY=minio123 \
    -e KP_OBJECT_STORE_BUCKET=default \
    -e KP_OBJECT_STORE_SIGNED_URL_EXPIRY=60 \
    --network kernel-planckster_default \
    maany/kernel-planckster
```

## Follow the logs
```bash
docker logs -f kernel-planckster
```

## Stop the Docker container
```bash
docker stop kernel-planckster && docker rm kernel-planckster
```

## Bring down the dependencies
```bash
docker compose -f docker-compose.yml --profile storage down
```