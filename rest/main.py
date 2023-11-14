from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any, Generic
from fastapi import APIRouter, FastAPI
import subprocess

from fastapi.responses import JSONResponse
from lib.core.sdk.caps_fastapi import FastAPIFeature
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseResponse
from lib.core.sdk.viewmodel import BaseErrorViewModel, BaseSuccessViewModel

from rest.config import Settings


class DemoSuccessViewModel(BaseSuccessViewModel):
    id: int | None = None


class DemoErrorViewModel(BaseErrorViewModel):
    pass


class DemoPresenter:
    def present_success(self, response: BaseResponse) -> DemoSuccessViewModel:
        return DemoSuccessViewModel(status=True, id=1)

    def present_error(self, response: BaseErrorResponse) -> DemoErrorViewModel:
        return DemoErrorViewModel(
            status=False,
            errorCode=response.errorCode,
            errorMessage=response.errorMessage,
            errorName=response.errorName,
            errorType=response.errorType,
        )


class DemoFeature(FastAPIFeature):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        # self.presenter: DemoPresenter = DemoPresenter()


demoFeature = DemoFeature(
    name="Demo",
    description="Demo Feature",
    group="demo",
    verb="GET",
    endpoint="/endpoint",
    # presenter_class=DemoPresenter,
)


@asynccontextmanager
async def load_features(app: FastAPI) -> Any:
    router: APIRouter | None = demoFeature.router
    if router is not None:
        app.router.include_router(router)
    yield None


app = FastAPI(lifespan=load_features)


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
