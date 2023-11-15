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
    def create_request(self, parameters: TBaseControllerParameters) -> TBaseRequest:
        raise NotImplementedError("You must implement the create_request method in your controller")

    def execute(self, parameters: BaseControllerParameters) -> TBaseViewModel | None:
        # data = self.presenter.present_success(response=BaseResponse(status=True, result="Hello World!"))
        data = self.presenter.present_error(
            BaseErrorResponse(
                status=False, code=500, errorCode=500, errorMessage="Error", errorName="Error", errorType="Error"
            )
        )
        return data


# class BaseController(ABC, Generic[TBaseControllerParameters, TBaseRequest]):
#     def __init__(
#         self,
#         usecase: BaseUseCase[TBaseRequest, TBaseResponse, TBaseErrorResponse],
#         presenter: Presentable[TBaseResponse, TBaseErrorResponse, TBaseViewModel],
#     ) -> None:
#         super().__init__()
#         self.usecase = usecase
#         self.presenter = presenter

#     @abstractmethod
#     def create_request(self, parameters: TBaseControllerParameters) -> TBaseRequest:
#         raise NotImplementedError("You must implement the create_request method in your controller")

#     def execute(self, parameters: TBaseControllerParameters) -> TBaseViewModel | None:
#         request = self.create_request(parameters)
#         response = self.usecase.execute(request)
#         view_model: TBaseViewModel
#         if response.status:
#             view_model = self.presenter.present_success(response)  # type: ignore
#         else:
#             view_model = self.presenter.present_error(response)  # type: ignore
#         return view_model


# TBaseController = TypeVar("TBaseController", bound=BaseController[BaseControllerParameters, BaseRequest])


# class DummyControllerParameters(BaseControllerParameters):
#     input: int = 0


# class DummyController(BaseController[DummyControllerParameters, DummyRequest]):
#     def __init__(
#         self,
#         usecase: BaseUseCase[DummyRequest, TBaseResponse, TBaseErrorResponse],
#         presenter: Presentable[TBaseResponse, TBaseErrorResponse, TBaseViewModel],
#     ) -> None:
#         super().__init__(usecase, presenter)

#     def create_request(self, parameters: DummyControllerParameters) -> DummyRequest:
#         return DummyRequest(number=parameters.input)


# TDummyController = TypeVar("TDummyController", bound=DummyController)
