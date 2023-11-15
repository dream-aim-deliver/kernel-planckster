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
    def execute(self, request: TBaseRequest) -> TBaseResponse | TBaseErrorResponse:
        """
        A base class for use case

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError("You must implement the execute method in your use case")


TBaseUseCase = TypeVar("TBaseUseCase", bound=BaseUseCase[BaseRequest, BaseResponse, BaseErrorResponse])
