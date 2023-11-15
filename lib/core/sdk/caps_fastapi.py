from abc import abstractmethod
from typing import Annotated, Any, Dict, Generic, Literal, Type, TypeVar
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, ConfigDict, Field, model_validator, validator
from lib.core.sdk.controller import BaseControllerParameters, TBaseControllerParameters
from lib.core.sdk.feature import BaseFeature

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
    BaseFeature[TBaseControllerParameters, TBaseRequest, TBaseResponse, TBaseErrorResponse, TBaseViewModel],
    Generic[TBaseControllerParameters, TBaseRequest, TBaseResponse, TBaseErrorResponse, TBaseViewModel],
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
        cls,
        instance: "FastAPIFeature[BaseControllerParameters, BaseRequest, BaseResponse, BaseErrorResponse, BaseViewModel]",
    ) -> "FastAPIFeature[BaseControllerParameters, BaseRequest, BaseResponse, BaseErrorResponse, BaseViewModel]":
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

    def handle_request(
        self,
        controller_parameters: TBaseControllerParameters | None = None,
    ) -> TBaseViewModel:
        controller = self.controller_factory()
        view_model = controller.execute(controller_parameters)
        if view_model is None:
            raise HTTPException(
                status_code=500,
                detail=f"Something went wrong. Controller for {self.verb} {self.endpoint} of feature {self.name} did not produce a view model.",
            )
        if not view_model.status:
            raise HTTPException(status_code=500, detail=view_model)
        else:
            return view_model

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
