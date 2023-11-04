from abc import ABC, abstractmethod
from typing import Generic

from lib.core.sdk.usecase_models import TBaseErrorResponse, TBaseRequest, TBaseResponse


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
