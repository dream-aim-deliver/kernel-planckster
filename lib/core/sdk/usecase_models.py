from typing import TypeVar
from pydantic import BaseModel


class BaseRequest(BaseModel):
    pass


TBaseRequest = TypeVar("TBaseRequest", bound=BaseRequest)


class BaseResponse(BaseModel):
    """
    Base response model for all use cases.

    @param status: The status of the response. Equals True.
    """

    status: bool = True


TBaseResponse = TypeVar("TBaseResponse", bound=BaseResponse)


class BaseErrorResponse(BaseResponse):
    """
    Base error response model for all use cases.

    @param status: The status of the response. Equals False.
    @param errorCode: The error code of the response.
    @param errorMessage: The error message of the response.
    @param errorName: The name of the error.
    @param errorType: The type of the error.
    """

    status: bool = False
    errorCode: int
    errorMessage: str
    errorName: str
    errorType: str


TBaseErrorResponse = TypeVar("TBaseErrorResponse", bound=BaseErrorResponse)
