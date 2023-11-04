from abc import ABC, abstractmethod
from typing import Generic

from lib.core.sdk.usecase_models import TBaseErrorResponse, TBaseResponse
from lib.core.sdk.viewmodel import TBaseViewModel


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
