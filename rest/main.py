from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any, Generic, TypeVar
from fastapi import APIRouter, FastAPI, HTTPException
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
    carahlo: str | None = None


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

    def endpoint_fn(self, request: Any) -> DemoSuccessViewModel:
        presenter = self.presenter
        if presenter is None:
            raise HTTPException(status_code=500, detail="Presenter is not defined")
        else:
            data = presenter.present_success(response=BaseResponse(status=True, result="Hello World!"))
            return data


demoFeature: FastAPIFeature[DemoSuccessViewModel] = DemoFeature(
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


T = TypeVar("T", bound=BaseSuccessViewModel, covariant=True)


class RealViewModel(BaseSuccessViewModel):  # DemoSuccessViewModel
    test: str | None = None


TRealViewModel = TypeVar("TRealViewModel", bound=RealViewModel, covariant=True)


class FastAPIViewModelWrapper(BaseModel, Generic[T]):  # FastAPIViewModelWrapper
    data: T | None = None


@app.get("/")
def read_root() -> FastAPIViewModelWrapper[TRealViewModel]:
    response: FastAPIViewModelWrapper[TRealViewModel] = FastAPIViewModelWrapper(
        status=True, id=1, name="Hello World!", test="Hello World!", data=RealViewModel(), a=1
    )
    return response


def server() -> None:
    settings = get_settings()
    cmd = ["uvicorn", "main:app", "--reload", "--host", f"{settings.host}", "--port", f"{settings.port}"]
    subprocess.run(cmd)
