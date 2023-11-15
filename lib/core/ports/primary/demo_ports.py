from abc import abstractmethod
from typing import Generic, Protocol
from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.primary_ports import BaseOutputPort

from lib.core.sdk.usecase_models import TBaseErrorResponse, TBaseRequest, TBaseResponse
from lib.core.sdk.viewmodel import TBaseViewModel


class DemoOutputPort(
    BasePresenter[TBaseResponse, TBaseErrorResponse, TBaseViewModel],
    Generic[TBaseResponse, TBaseErrorResponse, TBaseViewModel],
):
    @abstractmethod
    def convert_error_response_to_view_model(self, response: TBaseErrorResponse) -> TBaseViewModel:
        raise NotImplementedError(
            "You must implement the convert_error_response_to_view_model method in your presenter"
        )

    @abstractmethod
    def convert_response_to_view_model(self, response: TBaseResponse) -> TBaseViewModel:
        raise NotImplementedError("You must implement the convert_response_to_view_model method in your presenter")
