from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from lib.core.sdk.usecase_models import (
    BaseErrorResponse,
    BaseRequest,
    BaseResponse,
    TBaseErrorResponse,
    TBaseRequest,
    TBaseResponse,
)


class BaseUseCase(ABC, Generic[TBaseRequest, TBaseResponse, TBaseErrorResponse]):
    @abstractmethod
    def validate_request(self, request: TBaseRequest) -> bool:
        """
        A base class for use case

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError("You must implement the validate_request method in your use case")

    @abstractmethod
    def execute(self, request: TBaseRequest) -> TBaseResponse | TBaseErrorResponse:
        """
        A base class for use case

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError("You must implement the execute method in your use case")


TBaseUseCase = TypeVar("TBaseUseCase", bound=BaseUseCase[BaseRequest, BaseResponse, BaseErrorResponse])


class DummyRequest(BaseRequest):
    number: int = 0


class DummyResponse(BaseResponse):
    result: int | None = None


class DummyErrorResponse(BaseErrorResponse):
    pass


class DummyUseCase(BaseUseCase[DummyRequest, DummyResponse, DummyErrorResponse]):
    def validate_request(self, request: DummyRequest) -> bool:
        return True

    def execute(self, request: DummyRequest) -> DummyResponse | DummyErrorResponse:
        return DummyResponse(status=True, result=request.number * 2)
