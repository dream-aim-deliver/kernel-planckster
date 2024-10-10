from typing import Any

from fastapi import HTTPException
from pydantic import ValidationError
from lib.core.sdk.fastapi import FastAPIEndpoint
from lib.core.view_model.new_conversation_view_model import NewConversationViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.new_conversation_controller import NewConversationControllerParameters

from dependency_injector.wiring import inject, Provide


class NewConversationFastAPIFeature(FastAPIEndpoint[NewConversationControllerParameters, NewConversationViewModel]):
    @inject
    def __init__(
        self,
        descriptor: Any = Provide[ApplicationContainer.new_conversation_feature.feature_descriptor],
        controller: Any = Provide[ApplicationContainer.new_conversation_feature.controller],
    ):
        responses: dict[int | str, dict[str, Any]] = {
            200: {
                "model": NewConversationViewModel,
                "description": "Success",
            },
            400: {
                "model": NewConversationViewModel,
                "description": "Bad Request.",
            },
            500: {
                "model": NewConversationViewModel,
                "description": "Internal Server Error",
            },
        }

        super().__init__(controller=controller, descriptor=descriptor, responses=responses)

    def register_endpoint(self) -> None:
        @self.router.post(
            name=self.name,
            description=self.descriptor.description,
            path="/research-context/{id}/conversation",
            responses=self.responses,
        )
        def endpoint(
            id: int,
            conversation_title: str,
        ) -> NewConversationViewModel | None:
            try:
                controller_parameters = NewConversationControllerParameters(
                    research_context_id=id, conversation_title=conversation_title
                )
            except ValidationError as ve:
                raise HTTPException(status_code=400, detail=ve.errors())
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

            view_model: NewConversationViewModel = self.execute(
                controller_parameters=controller_parameters,
            )

            return view_model
