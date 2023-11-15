from typing import TypeVar
from pydantic import BaseModel


class BaseRequest(BaseModel):
    pass


TBaseRequest = TypeVar("TBaseRequest", bound=BaseRequest)


class BaseResponse(BaseModel):
    status: bool = True


TBaseResponse = TypeVar("TBaseResponse", bound=BaseResponse)
TBaseResponseContravariant = TypeVar("TBaseResponseContravariant", bound=BaseResponse, contravariant=True)


class BaseErrorResponse(BaseResponse):
    status: bool = False
    errorCode: int
    errorMessage: str
    errorName: str
    errorType: str


TBaseErrorResponse = TypeVar("TBaseErrorResponse", bound=BaseErrorResponse)
TBaseErrorResponseContravariant = TypeVar(
    "TBaseErrorResponseContravariant", bound=BaseErrorResponse, contravariant=True
)
