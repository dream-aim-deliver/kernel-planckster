from typing import Any
from lib.core.sdk.fastapi import FastAPIEndpoint
from lib.core.view_model.get_client_data_for_upload_view_model import GetClientDataForUploadViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.get_client_data_for_upload_controller import (
    GetClientDataForUploadControllerParameters,
)


from dependency_injector.wiring import inject, Provide


class GetClientDataForUploadFastAPIFeature(
    FastAPIEndpoint[GetClientDataForUploadControllerParameters, GetClientDataForUploadViewModel]
):
    @inject
    def __init__(
        self,
        descriptor: Any = Provide[ApplicationContainer.get_client_data_for_upload_feature.feature_descriptor],
        controller: Any = Provide[ApplicationContainer.get_client_data_for_upload_feature.controller],
    ):
        responses: dict[int | str, dict[str, Any]] = {
            200: {
                "model": GetClientDataForUploadViewModel,
                "description": "Success",
            },
            400: {
                "model": GetClientDataForUploadViewModel,
                "description": "Bad Request.",
            },
            500: {
                "model": GetClientDataForUploadViewModel,
                "description": "Internal Server Error",
            },
        }

        super().__init__(controller=controller, descriptor=descriptor, responses=responses)

    def register_endpoint(self) -> None:
        @self.router.get(
            name=self.name,
            description=self.descriptor.description,
            path="/get_client_data_for_upload",
            responses=self.responses,
        )
        def endpoint(
            lfn: str,
        ) -> GetClientDataForUploadViewModel | None:
            controller_parameters = GetClientDataForUploadControllerParameters(lfn_str=lfn)

            view_model: GetClientDataForUploadViewModel = self.execute(
                controller_parameters=controller_parameters,
            )

            return view_model
