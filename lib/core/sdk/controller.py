from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel
from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase import BaseUseCase

from lib.core.sdk.usecase_models import BaseErrorResponse, TBaseErrorResponse, TBaseRequest, TBaseResponse
from lib.core.sdk.viewmodel import TBaseViewModel


class BaseControllerParameters(BaseModel):
    pass


TBaseControllerParameters = TypeVar("TBaseControllerParameters", bound=BaseControllerParameters)


class BaseController(
    ABC, Generic[TBaseControllerParameters, TBaseRequest, TBaseResponse, TBaseErrorResponse, TBaseViewModel]
):
    def __init__(
        self,
        usecase: BaseUseCase[TBaseRequest, TBaseResponse, TBaseErrorResponse],
        presenter: BasePresenter[TBaseResponse, TBaseErrorResponse, TBaseViewModel],
    ) -> None:
        super().__init__()
        self._presenter = presenter
        self._usecase = usecase

    @property
    def usecase(self) -> BaseUseCase[TBaseRequest, TBaseResponse, TBaseErrorResponse]:
        return self._usecase

    @property
    def presenter(self) -> BasePresenter[TBaseResponse, TBaseErrorResponse, TBaseViewModel]:
        return self._presenter

    @abstractmethod
    def create_request(self, parameters: TBaseControllerParameters | None) -> TBaseRequest:
        raise NotImplementedError("You must implement the create_request method in your controller")

    def execute(self, parameters: TBaseControllerParameters | None) -> TBaseViewModel | None:
        request_model = self.create_request(parameters)
        response_model = self.usecase.execute(request_model)
        if isinstance(response_model, BaseErrorResponse):
            return self.presenter.present_error(response_model)  # type: ignore
        else:
            return self.presenter.present_success(response_model)
