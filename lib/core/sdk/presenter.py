from abc import ABC, abstractmethod
from typing import Generic, Protocol, runtime_checkable

from pydantic import ValidationError
from lib.core.sdk.primary_ports import BaseOutputPort

from lib.core.sdk.usecase_models import (
    BaseErrorResponse,
    TBaseErrorResponse,
    TBaseResponse,
)
from lib.core.sdk.viewmodel import (
    TBaseViewModel,
    TBaseViewModel,
)


class BasePresenter(
    BaseOutputPort[TBaseResponse, TBaseErrorResponse, TBaseViewModel],
    Generic[TBaseResponse, TBaseErrorResponse, TBaseViewModel],
):
    def present_success(self, response: TBaseResponse) -> TBaseViewModel:
        try:
            view_model = self.convert_response_to_view_model(response)
            return view_model
        except ValidationError as error:
            return self.convert_error_response_to_view_model(
                BaseErrorResponse(  # type: ignore
                    errorCode=500,
                    errorName="ValidationError",
                    errorMessage="ValidationError",
                    errorType="ValidationError",
                )
            )

    def present_error(self, response: TBaseErrorResponse) -> TBaseViewModel:
        return self.convert_error_response_to_view_model(response)

    @abstractmethod
    def convert_error_response_to_view_model(self, response: TBaseErrorResponse) -> TBaseViewModel:
        raise NotImplementedError(
            "You must implement the convert_error_response_to_view_model method in your presenter"
        )

    @abstractmethod
    def convert_response_to_view_model(self, response: TBaseResponse) -> TBaseViewModel:
        raise NotImplementedError("You must implement the convert_response_to_view_model method in your presenter")
