from typing import Any
from lib.core.sdk.fastapi import FastAPIEndpoint
from lib.core.view_model.upload_file_view_model import UploadFileViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.upload_file_controller import UploadFileControllerParameters


from dependency_injector.wiring import inject, Provide


class UploadFileFastAPIFeature(FastAPIEndpoint[UploadFileControllerParameters, UploadFileViewModel]):
    @inject
    def __init__(
        self,
        descriptor: Any = Provide[ApplicationContainer.upload_file_feature.feature_descriptor],
        controller: Any = Provide[ApplicationContainer.upload_file_feature.controller],
    ):
        responses: dict[int | str, dict[str, Any]] = {
            200: {
                "model": UploadFileViewModel,
                "description": "Success",
            },
            400: {
                "model": UploadFileViewModel,
                "description": "Bad Request.",
            },
            500: {
                "model": UploadFileViewModel,
                "description": "Internal Server Error",
            },
        }

        super().__init__(controller=controller, descriptor=descriptor, responses=responses)

    def register_endpoint(self) -> None:
        @self.router.get(
            name=self.name,
            description=self.descriptor.description,
            path="/upload_file",
            responses=self.responses,
        )
        def endpoint(
            file_path: str,
        ) -> UploadFileViewModel | None:
            controller_parameters = UploadFileControllerParameters(file_path=file_path)

            view_model: UploadFileViewModel = self.execute(
                controller_parameters=controller_parameters,
            )

            return view_model
