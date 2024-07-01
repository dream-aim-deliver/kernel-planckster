from typing import Any
from lib.core.sdk.fastapi import FastAPIEndpoint
from lib.core.view_model.new_research_context_view_mode import NewResearchContextViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.extend_research_context_controller import ExtendResearchContextControllerParameters

from dependency_injector.wiring import inject, Provide


class ExtendResearchContextFastAPIFeature(
    FastAPIEndpoint[ExtendResearchContextControllerParameters, NewResearchContextViewModel]
):
    @inject
    def __init__(
        self,
        descriptor: Any = Provide[ApplicationContainer.extend_research_context_feature.feature_descriptor],
        controller: Any = Provide[ApplicationContainer.extend_research_context_feature.controller],
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
            path="/research-context/extend",
            responses=self.responses,
        )
        def endpoint(
            new_research_context_title: str,
            new_research_context_description: str,
            new_source_data_ids: list[int],
            existing_research_context_id: int,
            client_sub: str,
            llm_name: str,
        ) -> NewResearchContextViewModel | None:
            controller_parameters = ExtendResearchContextControllerParameters(
                new_research_context_title=new_research_context_title,
                new_research_context_description=new_research_context_description,
                existing_research_context_id=existing_research_context_id,
                client_sub=client_sub,
                llm_name=llm_name,
                new_source_data_ids=new_source_data_ids,
            )

            view_model: NewResearchContextViewModel = self.execute(
                controller_parameters=controller_parameters,
            )

            return view_model
