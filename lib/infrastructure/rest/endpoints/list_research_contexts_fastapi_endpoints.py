from typing import Any
from lib.core.sdk.fastapi import FastAPIEndpoint
from lib.core.view_model.list_research_contexts_view_model import ListResearchContextsViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.list_research_contexts_controller import ListResearchContextsControllerParameters

from dependency_injector.wiring import inject, Provide


class ListResearchContextsFastAPIFeature(
    FastAPIEndpoint[ListResearchContextsControllerParameters, ListResearchContextsViewModel]
):
    @inject
    def __init__(
        self,
        descriptor: Any = Provide[ApplicationContainer.list_research_contexts_feature.feature_descriptor],
        controller: Any = Provide[ApplicationContainer.list_research_contexts_feature.controller],
    ):
        responses: dict[int | str, dict[str, Any]] = {
            200: {
                "model": ListResearchContextsViewModel,
                "description": "Success",
            },
            400: {
                "model": ListResearchContextsViewModel,
                "description": "Bad Request. User ID does not exist",
            },
            500: {
                "model": ListResearchContextsViewModel,
                "description": "Internal Server Error",
            },
        }

        super().__init__(controller=controller, descriptor=descriptor, responses=responses)

    def register_endpoint(self) -> None:
        @self.router.get(
            name=self.name,
            description=self.descriptor.description,
            path="/user/{id}/research_contexts",
            responses=self.responses,
        )
        def endpoint(
            id: int,
        ) -> ListResearchContextsViewModel | None:
            controller_parameters = ListResearchContextsControllerParameters(
                user_id=id,
            )
            view_model: ListResearchContextsViewModel = self.execute(
                controller_parameters=controller_parameters,
            )
            return view_model
