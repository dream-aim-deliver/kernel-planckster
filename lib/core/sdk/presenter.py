from abc import ABC, abstractmethod
from typing import Any, Generic, Protocol, Type, TypeVar, Union, runtime_checkable

from pydantic import BaseModel, ConfigDict
from lib.core.sdk.usecase import DummyErrorResponse, DummyResponse

from lib.core.sdk.usecase_models import BaseErrorResponse, BaseResponse, TBaseErrorResponse, TBaseResponse
from lib.core.sdk.viewmodel import (
    TBaseViewModel,
    TBaseViewModel,
    BaseViewModel,
)


@runtime_checkable
class Presentable(Protocol[TBaseViewModel]):
    """
    A base class for presenters
    """

    def present_success(self, response: BaseResponse) -> TBaseViewModel:
        raise NotImplementedError("You must implement the present_success method in your presenter")

    def present_error(self, response: BaseErrorResponse) -> TBaseViewModel:
        raise NotImplementedError("You must implement the present_error method in your presenter")


# class BasePresenter(Generic[TBaseViewModel]):
#     def present_success(self, response: TBaseResponse) -> TBaseViewModel:
#         raise NotImplementedError("You must implement the present_success method in your presenter")

#     def present_error(self, response: TBaseErrorResponse) -> TBaseViewModel:
#         raise NotImplementedError("You must implement the present_error method in your presenter")


# TPresentable = TypeVar("TPresentable", bound=Presentable)


# class DummyViewModel(BaseSuccessViewModel):
#     id: int | None = None


# class DummyPresenter:
#     def present_success(self, response: DummyResponse) -> DummyViewModel:
#         return DummyViewModel(status=True, id=response.result)

#     def present_error(self, response: DummyErrorResponse) -> BaseErrorViewModel:
#         return BaseErrorViewModel(
#             status=False,
#             errorCode=response.errorCode,
#             errorMessage=response.errorMessage,
#             errorName=response.errorName,
#             errorType=response.errorType,
#         )


# class TestFeature(BaseModel):
#     presenter_class: Type[BasePresenter[BaseResponse, BaseErrorResponse, DummyViewModel, BaseErrorViewModel]]
#     model_config = ConfigDict(arbitrary_types_allowed=True)

#     def __init__(self, **data: Any) -> None:
#         super().__init__(**data)
#         presenter_class = self.presenter_class
#         if presenter_class is not None:
#             self.presenter: BasePresenter[
#                 BaseResponse, BaseErrorResponse, DummyViewModel, BaseErrorViewModel
#             ] = presenter_class()
#         self.register_endpoints()

#     def register_endpoints(self) -> None:
#         view_model: DummyViewModel = self.presenter.present_success(
#             response=BaseResponse(status=True, result="Hello World!")
#         )
#         print(view_model)


# class TestFeature(
#     BaseModel,
#     Generic[
#         TBaseResponse,
#         TBaseSuccessViewModel,
#     ],
# ):
#     name: str
#     presenter_class: Type[Presentable[BaseSuccessViewModel]]
#     model_config = ConfigDict(arbitrary_types_allowed=True)

#     def __init__(self, **data: Any) -> None:
#         super().__init__(**data)
#         presenter_class = self.presenter_class
#         self.presenter = presenter_class()
#         self.register_endpoints()

#     def register_endpoints(self) -> None:
#         view_model: BaseSuccessViewModel = self.presenter.present_success(
#             response=BaseResponse(status=True, result="Hello World!")
#         )
#         print(view_model)


# class DummyFeature(TestFeature[BaseResponse, DummyViewModel]):
#     def __init__(self, **data: Any) -> None:
#         data["presenter_class"] = DummyPresenter
#         super().__init__(**data)


# feature = DummyFeature(
#     name="Dummy Feature",
# )
