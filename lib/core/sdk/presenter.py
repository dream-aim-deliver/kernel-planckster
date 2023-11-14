from abc import ABC, abstractmethod
from typing import Any, Generic, Type, TypeVar, Union

from pydantic import BaseModel, ConfigDict
from lib.core.sdk.usecase import DummyErrorResponse, DummyResponse

from lib.core.sdk.usecase_models import BaseErrorResponse, BaseResponse, TBaseErrorResponse, TBaseResponse
from lib.core.sdk.viewmodel import (
    BaseErrorViewModel,
    TBaseErrorViewModel,
    TBaseSuccessViewModel,
    TBaseViewModel,
    BaseSuccessViewModel,
)


class BasePresenter(ABC, Generic[TBaseResponse, TBaseErrorResponse, TBaseSuccessViewModel, TBaseErrorViewModel]):
    """
    A base class for presenters
    """

    @abstractmethod
    def present_success(self, response: TBaseResponse) -> TBaseSuccessViewModel:
        raise NotImplementedError("You must implement the present_success method in your presenter")

    @abstractmethod
    def present_error(self, response: TBaseErrorResponse) -> TBaseErrorViewModel:
        raise NotImplementedError("You must implement the present_error method in your presenter")


class DummyViewModel(BaseSuccessViewModel):
    id: int | None = None


class DummyPresenter(BasePresenter[DummyResponse, DummyErrorResponse, DummyViewModel, BaseErrorViewModel]):
    def present_success(self, response: DummyResponse) -> DummyViewModel:
        return DummyViewModel(status=True, id=response.result)

    def present_error(self, response: DummyErrorResponse) -> BaseErrorViewModel:
        return BaseErrorViewModel(
            status=False,
            errorCode=response.errorCode,
            errorMessage=response.errorMessage,
            errorName=response.errorName,
            errorType=response.errorType,
        )


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


class TestFeature(BaseModel, Generic[TBaseResponse, TBaseSuccessViewModel]):
    presenter_class: Type[BasePresenter[TBaseResponse, BaseErrorResponse, TBaseSuccessViewModel, BaseErrorViewModel]]
    model_config = ConfigDict(arbitrary_types_allowed=True)

    class TestFeature(BaseModel, Generic[TBaseResponse, TBaseSuccessViewModel]):
        presenter_class: Type[
            BasePresenter[TBaseResponse, BaseErrorResponse, TBaseSuccessViewModel, BaseErrorViewModel]
        ]
        model_config = ConfigDict(arbitrary_types_allowed=True)

        def __init__(self, **data: Any) -> None:
            super().__init__(**data)
            presenter_class = self.presenter_class
            if presenter_class is not None:
                self.presenter: BasePresenter[
                    TBaseResponse, BaseErrorResponse, TBaseSuccessViewModel, BaseErrorViewModel
                ] = presenter_class()
            self.register_endpoints()

        def register_endpoints(self) -> None:
            view_model: TBaseSuccessViewModel = self.presenter.present_success(
                response=BaseResponse(status=True, result="Hello World!")
            )
            print(view_model)
