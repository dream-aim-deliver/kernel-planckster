from typing import Any, TypeVar
from pydantic import BaseModel, model_validator, root_validator, validator


class BaseViewModel(BaseModel):
    status: bool
    code: int
    errorCode: int | None = None
    errorMessage: str | None = None
    errorName: str | None = None
    errorType: str | None = None

    @model_validator(mode="after")  # type: ignore
    def error_fields_absent_in_successful_response(cls, values: "BaseViewModel") -> "BaseViewModel":
        v = values.status
        if v:
            if values.errorCode:
                raise ValueError("errorCode should not be present in a successful response")
            if values.errorMessage:
                raise ValueError("errorMessage should not be present in a successful response")
            if values.errorName:
                raise ValueError("errorName should not be present in a successful response")
            if values.errorType:
                raise ValueError("errorType should not be present in a successful response")
        else:
            if not values.errorCode:
                raise ValueError("errorCode should be present in an unsuccessful response")
            if not values.errorMessage:
                raise ValueError("errorMessage should be present in an unsuccessful response")
            if not values.errorName:
                raise ValueError("errorName should be present in an unsuccessful response")
            if not values.errorType:
                raise ValueError("errorType should be present in an unsuccessful response")
        if not v:
            if values.code != values.errorCode:
                raise ValueError("code should be equal to errorCode in an unsuccessful response")
            if values.code >= 200 and values.code < 300:
                raise ValueError("code should NOT be between 200 and 299 in an unsuccessful response")
        return values


TBaseViewModel = TypeVar("TBaseViewModel", bound=BaseViewModel, covariant=True)
