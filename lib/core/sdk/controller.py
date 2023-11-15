from abc import ABC, abstractmethod
from typing import Generic, Protocol, TypeVar, cast, runtime_checkable

from pydantic import BaseModel
from lib.core.sdk.presenter import Presentable
from lib.core.sdk.usecase import BaseUseCase, DummyRequest

from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest, TBaseErrorResponse, TBaseRequest, TBaseResponse
from lib.core.sdk.viewmodel import TBaseViewModel


class BaseControllerParameters(BaseModel):
    pass


TBaseControllerParameters = TypeVar("TBaseControllerParameters", bound=BaseControllerParameters)


class BaseController(ABC, Generic[TBaseControllerParameters, TBaseRequest, TBaseViewModel]):
    def __init__(self, presenter: Presentable[TBaseViewModel]) -> None:
        super().__init__()
        self._presenter = presenter

    @property
    def presenter(self) -> Presentable[TBaseViewModel]:
        return self._presenter

    @abstractmethod
    def create_request(self, parameters: TBaseControllerParameters | None) -> TBaseRequest:
        raise NotImplementedError("You must implement the create_request method in your controller")

    def execute(self, parameters: TBaseControllerParameters | None) -> TBaseViewModel | None:
        print("******************* ", parameters)
        # data = self.presenter.present_success(response=BaseResponse(status=True, result="Hello World!"))
        data = self.presenter.present_error(
            BaseErrorResponse(
                status=False, code=500, errorCode=500, errorMessage="Error", errorName="Error", errorType="Error"
            )
        )
        return data
