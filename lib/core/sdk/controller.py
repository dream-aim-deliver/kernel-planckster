from abc import ABC, abstractmethod
from typing import Generic, TypeVar, cast

from pydantic import BaseModel
from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase import BaseUseCase

from lib.core.sdk.usecase_models import TBaseErrorResponse, TBaseRequest, TBaseResponse
from lib.core.sdk.viewmodel import TBaseViewModel


class BaseControllerParameters(BaseModel):
    pass


TBaseControllerParameters = TypeVar("TBaseControllerParameters", bound=BaseControllerParameters)


class BaseController(ABC, Generic[TBaseControllerParameters, TBaseRequest]):
    def __init__(
        self,
        usecase: BaseUseCase[TBaseRequest, TBaseResponse, TBaseErrorResponse],
        presenter: BasePresenter[TBaseResponse, TBaseErrorResponse, TBaseViewModel],
    ) -> None:
        super().__init__()
        self.usecase = usecase
        self.presenter = presenter

    @abstractmethod
    def create_request(self, parameters: TBaseControllerParameters) -> TBaseRequest:
        raise NotImplementedError("You must implement the create_request method in your controller")

    def execute(self, parameters: TBaseControllerParameters) -> TBaseViewModel | None:
        request = self.create_request(parameters)
        response = self.usecase.execute(request)
        view_model: TBaseViewModel
        if response.status:
            view_model = cast(TBaseViewModel, self.presenter.present_success(response))
        else:
            view_model = self.presenter.present_error(response)
        return view_model
