from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any, Generic, TypeVar
from fastapi import APIRouter, FastAPI
import subprocess

from fastapi.responses import JSONResponse
from pydantic import BaseModel
from lib.core.sdk.caps_fastapi import FastAPIFeature
from lib.core.sdk.presenter import Presentable
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseResponse
from lib.core.sdk.viewmodel import BaseErrorViewModel, BaseSuccessViewModel

from rest.config import Settings


class DemoSuccessViewModel(BaseSuccessViewModel):
    test: str | None = None


TDemoSuccessViewModel = TypeVar("TDemoSuccessViewModel", bound=DemoSuccessViewModel, covariant=True)


class DemoErrorViewModel(BaseErrorViewModel):
    pass


class DemoPresenter:
    def present_success(self, response: BaseResponse) -> DemoSuccessViewModel:
        return DemoSuccessViewModel(status=True, id=1, test="This is a test")

    def present_error(self, response: BaseErrorResponse) -> DemoErrorViewModel:
        return DemoErrorViewModel(
            status=False,
            errorCode=response.errorCode,
            errorMessage=response.errorMessage,
            errorName=response.errorName,
            errorType=response.errorType,
        )


class DemoFeature(FastAPIFeature[DemoSuccessViewModel]):
    presenter: Presentable[DemoSuccessViewModel] = DemoPresenter()
    # model_config = FastAPIFeature.model_config

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)


demoFeature = DemoFeature(
    name="Demo",
    description="Demo Feature",
    group="demo",
    verb="GET",
    endpoint="/endpoint",
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


T = TypeVar("T", bound=BaseSuccessViewModel)


class RealT(BaseSuccessViewModel):  # DemoSuccessViewModel
    test: str | None = None


class TestViewModel(BaseModel, Generic[T]):  # FastAPIViewModelWrapper
    data: T | None = None


@app.get("/")
def read_root() -> TestViewModel[RealT]:
    response: TestViewModel[RealT] = TestViewModel(status=True, id=1, name="Hello World!", test="Hello World!")
    return response


def server() -> None:
    settings = get_settings()
    cmd = ["uvicorn", "main:app", "--reload", "--host", f"{settings.host}", "--port", f"{settings.port}"]
    subprocess.run(cmd)
