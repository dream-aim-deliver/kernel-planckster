from typing import Any

from fastapi import HTTPException
from pydantic import ValidationError
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
            client_sub: str,
            llm_name: str,
        ) -> CreateDefaultDataViewModel | None:
            try:
                controller_parameters = CreateDefaultDataControllerParameters(
                    client_sub=client_sub,
                    llm_name=llm_name,
                )
            except ValidationError as ve:
                raise HTTPException(status_code=400, detail=ve.errors())
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

            view_model: CreateDefaultDataViewModel = self.execute(
                controller_parameters=controller_parameters,
            )
            return view_model
