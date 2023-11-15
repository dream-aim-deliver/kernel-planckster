from abc import ABC, abstractmethod
from typing import Generic, Protocol, runtime_checkable

from lib.core.sdk.usecase_models import (
    TBaseErrorResponse,
    TBaseErrorResponseContravariant,
    TBaseResponse,
    TBaseResponseContravariant,
)
from lib.core.sdk.viewmodel import (
    TBaseViewModel,
    TBaseViewModel,
)


# @runtime_checkable
class Presentable(Generic[TBaseResponse, TBaseErrorResponse, TBaseViewModel]):
    """
    A base class for presenters
    """

    def present_success(self, response: TBaseResponse) -> TBaseViewModel:
        raise NotImplementedError("You must implement the present_success method in your presenter")

    def present_error(self, response: TBaseErrorResponse) -> TBaseViewModel:
        raise NotImplementedError("You must implement the present_error method in your presenter")
