from typing import Union, TypeVar
from pydantic import BaseModel


class BaseSuccessViewModel(BaseModel):
    status: bool = True


TBaseSuccessViewModel = TypeVar("TBaseSuccessViewModel", bound=BaseSuccessViewModel, covariant=True)


class BaseErrorViewModel(BaseModel):
    status: bool = False
    errorCode: int
    errorMessage: str
    errorName: str
    errorType: str


TBaseErrorViewModel = TypeVar("TBaseErrorViewModel", bound=BaseErrorViewModel)

TBaseViewModel = Union[TBaseSuccessViewModel, TBaseErrorViewModel]
