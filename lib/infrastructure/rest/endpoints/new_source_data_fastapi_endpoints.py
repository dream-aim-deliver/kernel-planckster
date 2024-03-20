from typing import Any
from lib.core.entity.models import KnowledgeSource
from lib.core.sdk.fastapi import FastAPIEndpoint
from lib.core.view_model.new_source_data_view_model import NewSourceDataViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.new_source_data_controller import NewSourceDataControllerParameters

from dependency_injector.wiring import inject, Provide


class NewSourceDataFastAPIFeature(FastAPIEndpoint[NewSourceDataControllerParameters, NewSourceDataViewModel]):
    @inject
    def __init__(
        self,
        descriptor: Any = Provide[ApplicationContainer.new_source_data_feature.feature_descriptor],
        controller: Any = Provide[ApplicationContainer.new_source_data_feature.controller],
    ):
        responses: dict[int | str, dict[str, Any]] = {
            200: {
                "model": NewSourceDataViewModel,
                "description": "Success",
            },
            400: {
                "model": NewSourceDataViewModel,
                "description": "Bad Request. Research Context ID does not exist",
            },
            500: {
                "model": NewSourceDataViewModel,
                "description": "Internal Server Error",
            },
        }

        super().__init__(controller=controller, descriptor=descriptor, responses=responses)

    def register_endpoint(self) -> None:
        @self.router.post(
            name=self.name,
            description=self.descriptor.description,
            path="/knowledge_source/{id}/source_data",
            responses=self.responses,
        )
        def endpoint(
            id: int,
            lfn: str,
        ) -> NewSourceDataViewModel | None:
            controller_parameters = NewSourceDataControllerParameters(knowledge_source_id=id, lfn=lfn)
            view_model: NewSourceDataViewModel = self.execute(
                controller_parameters=controller_parameters,
            )
            return view_model
