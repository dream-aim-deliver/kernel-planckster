from typing import Any
from lib.core.sdk.fastapi import FastAPIEndpoint
from lib.core.view_model.new_research_context_view_mode import NewResearchContextViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.new_research_context_controller import NewResearchContextControllerParameters

from dependency_injector.wiring import inject, Provide


class NewResearchContextFastAPIFeature(
    FastAPIEndpoint[NewResearchContextControllerParameters, NewResearchContextViewModel]
):
    @inject
    def __init__(
        self,
        descriptor: Any = Provide[ApplicationContainer.new_research_context_feature.feature_descriptor],
        controller: Any = Provide[ApplicationContainer.new_research_context_feature.controller],
    ):
        responses: dict[int | str, dict[str, Any]] = {
            200: {
                "model": NewResearchContextViewModel,
                "description": "Success",
            },
            400: {
                "model": NewResearchContextViewModel,
                "description": "Bad Request.",
            },
            500: {
                "model": NewResearchContextViewModel,
                "description": "Internal Server Error",
            },
        }

        super().__init__(controller=controller, descriptor=descriptor, responses=responses)

    def register_endpoint(self) -> None:
        @self.router.post(
            name=self.name,
            description=self.descriptor.description,
            path="/research-context",
            responses=self.responses,
        )
        def endpoint(
            research_context_title: str,
            research_context_description: str,
            source_data_ids: list[int],
            client_sub: str | None = None,
            llm_name: str | None = None,
        ) -> NewResearchContextViewModel | None:
            controller_parameters = NewResearchContextControllerParameters(
                research_context_title=research_context_title,
                research_context_description=research_context_description,
                client_sub=client_sub,
                llm_name=llm_name,
                source_data_ids=source_data_ids,
            )

            view_model: NewResearchContextViewModel = self.execute(
                controller_parameters=controller_parameters,
            )

            return view_model
