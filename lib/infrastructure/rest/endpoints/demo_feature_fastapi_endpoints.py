from typing import Any

from lib.core.sdk.fastapi import FastAPIEndpoint

from lib.core.view_model.demo_view_model import DemoViewModel
from lib.infrastructure.controller.demo_controller import DemoControllerParameters
from lib.infrastructure.config.containers import ApplicationContainer

from dependency_injector.wiring import inject, Provide


class DemoFastAPIFeature(FastAPIEndpoint[DemoControllerParameters, DemoViewModel]):
    @inject
    def __init__(
        self,
        descriptor: Any = Provide[ApplicationContainer.demo_feature.feature_descriptor],
        controller: Any = Provide[ApplicationContainer.demo_feature.controller],
    ):
        responses: dict[int | str, dict[str, Any]] = {
            200: {
                "model": DemoViewModel,
                "description": "Success",
            },
            400: {
                "model": DemoViewModel,
                "description": "Bad Request",
            },
            500: {
                "model": DemoViewModel,
                "description": "Internal Server Error",
            },
        }

        super().__init__(controller=controller, descriptor=descriptor, responses=responses)

    def register_endpoint(self) -> None:
        @self.router.get(
            name=self.name,
            description=self.descriptor.description,
            path="/sum",
            responses=self.responses,
        )
        def endpoint(num1: int, num2: int) -> DemoViewModel | None:
            controller_parameters = DemoControllerParameters(num1=num1, num2=num2)
            view_model: DemoViewModel = self.execute(
                controller_parameters=controller_parameters,
            )
            return view_model
