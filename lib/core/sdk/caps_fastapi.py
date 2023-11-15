from abc import abstractmethod
from typing import Annotated, Any, Dict, Generic, Literal, Type, TypeVar
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, ConfigDict, Field, model_validator, validator
from lib.core.sdk.controller import BaseControllerParameters, TBaseControllerParameters
from lib.core.sdk.feature import BaseFeature

from lib.core.sdk.presenter import Presentable
from lib.core.sdk.usecase_models import (
    BaseErrorResponse,
    BaseRequest,
    BaseResponse,
    TBaseErrorResponse,
    TBaseRequest,
    TBaseResponse,
)
from lib.core.sdk.viewmodel import (
    BaseViewModel,
    TBaseViewModel,
    TBaseViewModel,
)

T = TypeVar("T", bound=BaseViewModel)


class FastAPIViewModelWrapper(BaseModel, Generic[T]):
    data: T | None = None


class FastAPIFeature(
    BaseFeature[TBaseControllerParameters, TBaseRequest, TBaseViewModel],
    Generic[TBaseControllerParameters, TBaseRequest, TBaseViewModel],
):
    group: str
    responses: Dict[int | str, dict[str, Any]] | None = None
    auth_required: bool = False
    router: APIRouter | None = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    @model_validator(mode="after")  # type: ignore
    def populate_arbitrary_fields(
        cls, instance: "FastAPIFeature[BaseControllerParameters, BaseRequest, BaseViewModel]"
    ) -> "FastAPIFeature[BaseControllerParameters, BaseRequest, BaseViewModel]":
        group = instance.group
        instance.router = APIRouter(prefix=f"/{group}", tags=[group])
        instance.register_endpoints(instance.router)

    @abstractmethod
    def endpoint_fn(
        self,
        request: Request,
        response: Response,
        request_query_parameters: TBaseControllerParameters | None = None,
        request_body_parameters: TBaseRequest | None = None,
    ) -> TBaseViewModel:
        raise NotImplementedError("You must implement the endpoint_fn method in your feature")

    # TODO: Controller Parameters type injection  https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/#shortcut
    def handle_request(
        self,
        controller_parameters: TBaseControllerParameters | None = None,
    ) -> TBaseViewModel:
        controller = self.controller_factory()
        controller.execute(controller_parameters)
        # controller.execute(query)
        presenter = self.presenter_factory()
        if presenter is None:
            raise HTTPException(status_code=500, detail="Presenter is not defined")
        else:
            # data = presenter.present_success(response=BaseResponse(status=True, result="Hello World!"))
            data = presenter.present_error(
                BaseErrorResponse(
                    status=False, code=500, errorCode=500, errorMessage="Error", errorName="Error", errorType="Error"
                )
            )
            # response.status_code = data.code
            return data

    def register_endpoints(self, router: APIRouter) -> None:
        router.add_api_route(
            methods=[self.verb],
            tags=[self.group],
            path=f"{self.endpoint}",
            name=self.name,
            description=self.description,
            endpoint=self.endpoint_fn,
            responses=self.responses,
        )
