from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any, Generic, Literal, TypeVar
from fastapi import APIRouter, FastAPI, HTTPException, Request, Response
import subprocess

from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from lib.core.sdk.caps_fastapi import FastAPIFeature
from lib.core.sdk.presenter import Presentable
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseResponse
from lib.core.sdk.viewmodel import BaseViewModel

from rest.config import Settings


class DemoViewModel(BaseViewModel):
    test: str | None = None
    carahlo: str | None = None


TDemoSuccessViewModel = TypeVar("TDemoSuccessViewModel", bound=DemoViewModel, covariant=True)


class DemoPresenter:
    def present_success(self, response: BaseResponse) -> DemoViewModel:
        return DemoViewModel(status=True, code=200, id=1, test="This is a test")

    def present_error(self, response: BaseErrorResponse) -> DemoViewModel:
        return DemoViewModel(
            status=False,
            code=response.errorCode,
            errorCode=response.errorCode,
            errorMessage=response.errorMessage,
            errorName=response.errorName,
            errorType=response.errorType,
        )


class DemoFeature(FastAPIFeature[DemoViewModel]):
    name: str = "Demo"
    description: str = "Demo Feature"
    group: str = "demo"
    verb: Literal["GET", "POST", "PUT", "DELETE"] = "GET"
    endpoint: str = "/endpoint"
    presenter: Presentable[DemoViewModel] = DemoPresenter()

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

    def endpoint_fn(self, request: Request, response: Response) -> DemoViewModel:
        presenter = self.presenter
        name = self.name
        if presenter is None:
            raise HTTPException(status_code=500, detail="Presenter is not defined")
        else:
            # data = presenter.present_success(response=BaseResponse(status=True, result="Hello World!"))
            data = presenter.present_error(
                BaseErrorResponse(
                    status=False, code=500, errorCode=500, errorMessage="Error", errorName="Error", errorType="Error"
                )
            )
            return data


demoFeature: FastAPIFeature[DemoViewModel] = DemoFeature()


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


T = TypeVar("T", bound=BaseViewModel, covariant=True)


class RealViewModel(BaseViewModel):  # DemoSuccessViewModel
    test: str | None = None


TRealViewModel = TypeVar("TRealViewModel", bound=RealViewModel, covariant=True)


class FastAPIViewModelWrapper(BaseModel, Generic[T]):  # FastAPIViewModelWrapper
    data: T | None = None


@app.get("/")
def read_root() -> FastAPIViewModelWrapper[TRealViewModel]:
    response: FastAPIViewModelWrapper[TRealViewModel] = FastAPIViewModelWrapper(
        status=True,
        code=200,
        id=1,
        name="Hello World!",
        test="Hello World!",
        data=RealViewModel(status=True, code=200),
        a=1,
    )
    return response


def server() -> None:
    settings = get_settings()
    cmd = ["uvicorn", "main:app", "--reload", "--host", f"{settings.host}", "--port", f"{settings.port}"]
    subprocess.run(cmd)
