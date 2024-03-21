from typing import Any
from lib.core.sdk.fastapi import FastAPIEndpoint
from lib.core.view_model.get_client_data_for_download_view_model import GetClientDataForDownloadViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.get_client_data_for_download_controller import (
    GetClientDataForDownloadControllerParameters,
)


from dependency_injector.wiring import inject, Provide


class GetClientDataForDownloadFastAPIFeature(
    FastAPIEndpoint[GetClientDataForDownloadControllerParameters, GetClientDataForDownloadViewModel]
):
    @inject
    def __init__(
        self,
        descriptor: Any = Provide[ApplicationContainer.get_client_data_for_download_feature.feature_descriptor],
        controller: Any = Provide[ApplicationContainer.get_client_data_for_download_feature.controller],
    ):
        responses: dict[int | str, dict[str, Any]] = {
            200: {
                "model": GetClientDataForDownloadViewModel,
                "description": "Success",
            },
            400: {
                "model": GetClientDataForDownloadViewModel,
                "description": "Bad Request.",
            },
            500: {
                "model": GetClientDataForDownloadViewModel,
                "description": "Internal Server Error",
            },
        }

        super().__init__(controller=controller, descriptor=descriptor, responses=responses)

    def register_endpoint(self) -> None:
        @self.router.get(
            name=self.name,
            description=self.descriptor.description,
            path="/get_client_data_for_download",
            responses=self.responses,
        )
        def endpoint(
            lfn: str,
        ) -> GetClientDataForDownloadViewModel | None:
            controller_parameters = GetClientDataForDownloadControllerParameters(lfn_str=lfn)

            view_model: GetClientDataForDownloadViewModel = self.execute(
                controller_parameters=controller_parameters,
            )

            return view_model
