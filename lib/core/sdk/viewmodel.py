from typing import Optional, TypeVar
from pydantic import BaseModel


class BaseViewModel(BaseModel):
    status: bool
    errorCode: int | None = None
    errorMessage: str | None = None
    errorName: str | None = None
    errorType: str | None = None


TBaseViewModel = TypeVar("TBaseViewModel", bound=BaseViewModel)
