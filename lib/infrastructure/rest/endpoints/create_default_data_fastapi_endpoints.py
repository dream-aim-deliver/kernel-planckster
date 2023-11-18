from typing import Any
from lib.core.sdk.fastapi import FastAPIEndpoint
from lib.core.view_model.create_default_data_view_model import CreateDefaultDataViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.create_default_data_controller import CreateDefaultDataControllerParameters


from dependency_injector.wiring import Provide, inject


class CreateDefaultDataFastAPIFeature(
    FastAPIEndpoint[CreateDefaultDataControllerParameters, CreateDefaultDataViewModel]
):
    @inject
    def __init__(
        self,
        descriptor: Any = Provide[ApplicationContainer.create_default_data_feature.feature_descriptor],
        controller: Any = Provide[ApplicationContainer.create_default_data_feature.controller],
    ):
        responses: dict[int | str, dict[str, Any]] = {
            200: {
                "model": CreateDefaultDataViewModel,
                "description": "Success",
            },
            400: {
                "model": CreateDefaultDataViewModel,
                "description": "Bad Request.",
            },
            500: {
                "model": CreateDefaultDataViewModel,
                "description": "Internal Server Error",
            },
        }

        super().__init__(controller=controller, descriptor=descriptor, responses=responses)

    def register_endpoint(self) -> None:
        @self.router.post(
            name=self.name,
            description=self.descriptor.description,
            path="/populate",
            responses=self.responses,
        )
        def endpoint(
            user_sid: str,
            llm_name: str,
        ) -> CreateDefaultDataViewModel | None:
            controller_parameters = CreateDefaultDataControllerParameters(
                user_sid=user_sid,
                llm_name=llm_name,
            )
            view_model: CreateDefaultDataViewModel = self.execute(
                controller_parameters=controller_parameters,
            )
            return view_model
