from typing import Any
from dependency_injector.wiring import inject, Provide

from lib.core.sdk.fastapi import FastAPIEndpoint
from lib.core.view_model.list_source_data_for_research_context_view_model import (
    ListSourceDataForResearchContextViewModel,
)
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.list_source_data_for_research_context_controller import (
    ListSourceDataForResearchContextControllerParameters,
)


class ListSourceDataForResearchContextFastAPIFeature(
    FastAPIEndpoint[ListSourceDataForResearchContextControllerParameters, ListSourceDataForResearchContextViewModel]
):
    @inject
    def __init__(
        self,
        descriptor: Any = Provide[
            ApplicationContainer.list_source_data_for_research_context_feature.feature_descriptor
        ],
        controller: Any = Provide[ApplicationContainer.list_source_data_for_research_context_feature.controller],
    ):
        responses: dict[int | str, dict[str, Any]] = {
            200: {
                "model": ListSourceDataForResearchContextViewModel,
                "description": "Success",
            },
            400: {
                "model": ListSourceDataForResearchContextViewModel,
                "description": "Bad Request.",
            },
            500: {
                "model": ListSourceDataForResearchContextViewModel,
                "description": "Internal Server Error",
            },
        }

        super().__init__(controller=controller, descriptor=descriptor, responses=responses)

    def register_endpoint(self) -> None:
        @self.router.get(
            name=self.name,
            description=self.descriptor.description,
            path="/research-context/{id}/source",
            responses=self.responses,
        )
        def endpoint(
            id: int,
        ) -> ListSourceDataForResearchContextViewModel | None:
            controller_parameters = ListSourceDataForResearchContextControllerParameters(
                research_context_id=id,
            )

            view_model: ListSourceDataForResearchContextViewModel = self.execute(
                controller_parameters=controller_parameters,
            )

            return view_model
