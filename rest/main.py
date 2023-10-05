from functools import lru_cache
from typing import Dict
from fastapi import FastAPI, Response
import subprocess

from fastapi.responses import JSONResponse

from rest.config import Settings

app = FastAPI()


@lru_cache()
def get_settings() -> Settings:
    return Settings()


@app.get("/")
def read_root() -> JSONResponse:
    response = JSONResponse(status_code=404, content="Not Found")
    return response


def server() -> None:
    settings = get_settings()
    cmd = ["uvicorn", "main:app", "--reload", "--host", f"{settings.host}", "--port", f"{settings.port}"]
    subprocess.run(cmd)
