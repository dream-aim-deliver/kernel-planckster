from typing import Generic, Optional, Literal, TypeVar, NewVar
from pydantic import BaseModel


TModel = NewVar("TModel")

class BaseDTO(BaseModel, Generic[TModel]):
    """
    A base DTO class for the project

    @param status:  
    @param errorCode: The error code of the operation
    @type errorCode: Optional[int]
    @param errorMessage: The error message of the operation
    @type errorMessage: Optional[str]
    @param errorName: The error name of the operation
    @type errorName: Optional[str]
    @param errorType: The error type of the operation
    @type errorType: Literal["gateway_endpoint_error"] | str | None
    """

    status: bool
    errorCode: Optional[int] = None
    errorMessage: Optional[str] = None
    errorName: Optional[str] = None
    errorType: Literal["gateway_endpoint_error"] | str | None = None
    data: Optional[]


TBaseDTO = TypeVar("TBaseDTO", bound=BaseDTO)
