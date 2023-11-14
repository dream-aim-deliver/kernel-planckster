from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from lib.core.sdk.usecase import DummyErrorResponse, DummyResponse

from lib.core.sdk.usecase_models import BaseErrorResponse, BaseResponse, TBaseErrorResponse, TBaseResponse
from lib.core.sdk.viewmodel import TBaseViewModel, BaseViewModel


class BasePresenter(ABC, Generic[TBaseResponse, TBaseErrorResponse, TBaseViewModel]):
    """
    A base class for presenters

    Raises:
        NotImplementedError: _description_
    """

    @abstractmethod
    def present_success(self, response: TBaseResponse) -> TBaseViewModel:
        raise NotImplementedError("You must implement the present_success method in your presenter")

    @abstractmethod
    def present_error(self, response: TBaseErrorResponse) -> TBaseViewModel:
        raise NotImplementedError("You must implement the present_error method in your presenter")


TBasePresenter = TypeVar("TBasePresenter", bound=BasePresenter[BaseResponse, BaseErrorResponse, BaseViewModel])


class DummyViewModel(BaseViewModel):
    id: int | None = None


class DummyPresenter(BasePresenter[DummyResponse, DummyErrorResponse, DummyViewModel]):
    def present_success(self, response: DummyResponse) -> DummyViewModel:
        return DummyViewModel(status=True, id=response.result)

    def present_error(self, response: DummyErrorResponse) -> DummyViewModel:
        return DummyViewModel(status=False, message=response.errorMessage)
