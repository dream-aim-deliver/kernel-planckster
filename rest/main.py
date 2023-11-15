from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any
from fastapi import APIRouter, FastAPI
import subprocess

from rest.config import Settings, FEATURES


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


@asynccontextmanager
async def load_features(app: FastAPI) -> Any:
    for feature in FEATURES:
        router: APIRouter | None = feature.router
        if router is not None:
            app.router.include_router(router)
    yield None


app = FastAPI(lifespan=load_features)


# T = TypeVar("T", bound=BaseViewModel, covariant=True)


# class RealViewModel(BaseViewModel):  # DemoSuccessViewModel
#     test: str | None = None


# TRealViewModel = TypeVar("TRealViewModel", bound=RealViewModel, covariant=True)


# class FastAPIViewModelWrapper(BaseModel, Generic[T]):  # FastAPIViewModelWrapper
#     data: T | None = None


# @app.get("/")
# def read_root() -> FastAPIViewModelWrapper[TRealViewModel]:
#     response: FastAPIViewModelWrapper[TRealViewModel] = FastAPIViewModelWrapper(
#         status=True,
#         code=200,
#         id=1,
#         name="Hello World!",
#         test="Hello World!",
#         data=RealViewModel(status=True, code=200),
#         a=1,
#     )
#     return response


def server() -> None:
    cmd = ["uvicorn", "main:app", "--reload", "--host", f"{settings.host}", "--port", f"{settings.port}"]
    subprocess.run(cmd)
