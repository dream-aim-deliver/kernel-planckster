from abc import ABC, abstractmethod
from typing import Generic

from lib.core.sdk.usecase_models import TBaseErrorResponse, TBaseRequest, TBaseResponse
from lib.core.sdk.viewmodel import TBaseViewModel


class BaseInputPort(ABC, Generic[TBaseRequest, TBaseResponse, TBaseErrorResponse]):
    @abstractmethod
    def execute(self, request: TBaseRequest) -> TBaseResponse | TBaseErrorResponse:
        raise NotImplementedError("This method must be implemented by the usecase.")


class BaseOutputPort(ABC, Generic[TBaseResponse, TBaseErrorResponse, TBaseViewModel]):
    @abstractmethod
    def present_success(self, response: TBaseResponse) -> TBaseViewModel:
        raise NotImplementedError("This method must be implemented by the presenter.")

    @abstractmethod
    def present_error(self, response: TBaseErrorResponse) -> TBaseViewModel:
        raise NotImplementedError("This method must be implemented by the presenter.")
