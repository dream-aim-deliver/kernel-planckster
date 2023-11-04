from typing import Optional, TypeVar
from pydantic import BaseModel


class BaseViewModel(BaseModel):
    status: bool
    errorCode: Optional[int]
    errorMessage: Optional[str]
    errorName: Optional[str]
    errorType: Optional[str]


TBaseViewModel = TypeVar("TBaseViewModel", bound=BaseViewModel)
