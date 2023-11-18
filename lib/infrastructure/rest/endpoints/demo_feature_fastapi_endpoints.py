from typing import Annotated, Any

from fastapi import Depends, Request, Response
from lib.core.sdk.fastapi import FastAPIEndpoint

from lib.core.sdk.feature_descriptor import BaseFeatureDescriptor
from lib.core.view_model.demo_view_model import DemoViewModel
from lib.infrastructure.controller.demo_controller import DemoController, DemoControllerParameters
from lib.infrastructure.config.containers import ApplicationContainer

from dependency_injector.wiring import inject, Provide


class DemoFastAPIQueryParameters(DemoControllerParameters):
    pass


class DemoFastAPIFeature(FastAPIEndpoint[DemoFastAPIQueryParameters, Any, DemoControllerParameters, DemoViewModel]):
    @inject
    def __init__(
        self,
        descriptor_provider: Any = Provide[ApplicationContainer.demo_feature.feature_descriptor.provider],
        controller_provider: Any = Provide[ApplicationContainer.demo_feature.controller.provider],
    ) -> None:
        descriptor: BaseFeatureDescriptor = descriptor_provider()
        controller: DemoController = controller_provider()
        super().__init__(
            name="Demo",
            controller=controller,
            descriptor=descriptor,
            responses={
                200: {
                    "model": DemoViewModel,
                    "description": "Success",
                },
                500: {
                    "model": DemoViewModel,
                    "description": "Internal Server Error",
                },
            },
        )

    def create_controller_parameters(
        self, query: DemoFastAPIQueryParameters | None, body: Any
    ) -> DemoControllerParameters:
        if query is None:
            return DemoControllerParameters(num1=0, num2=0)
        else:
            return DemoControllerParameters(num1=query.num1, num2=query.num2)

    def endpoint_fn(  # type: ignore
        self,
        request: Request,
        id: int,
        response: Response,
        request_query_parameters: Annotated[DemoFastAPIQueryParameters, Depends()],
    ) -> DemoViewModel | None:
        view_model: DemoViewModel | None = super().endpoint_fn(
            request=request,
            response=response,
            request_query_parameters=request_query_parameters,
        )
        return view_model
