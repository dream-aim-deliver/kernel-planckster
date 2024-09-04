from typing import Any, List
from lib.core.sdk.fastapi import FastAPIEndpoint
from lib.core.view_model.new_message_view_model import NewMessageViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.new_message_controller import NewMessageControllerParameters

from dependency_injector.wiring import inject, Provide


class NewMessageFastAPIFeature(FastAPIEndpoint[NewMessageControllerParameters, NewMessageViewModel]):
    @inject
    def __init__(
        self,
        descriptor: Any = Provide[ApplicationContainer.new_message_feature.feature_descriptor],
        controller: Any = Provide[ApplicationContainer.new_message_feature.controller],
    ):
        responses: dict[int | str, dict[str, Any]] = {
            200: {
                "model": NewMessageViewModel,
                "description": "Success",
            },
            400: {
                "model": NewMessageViewModel,
                "description": "Bad Request.",
            },
            500: {
                "model": NewMessageViewModel,
                "description": "Internal Server Error",
            },
        }

        super().__init__(controller=controller, descriptor=descriptor, responses=responses)

    def register_endpoint(self) -> None:
        @self.router.post(
            name=self.name,
            description=self.descriptor.description,
            path="/conversation/{id}/message",
            responses=self.responses,
        )
        def endpoint(
            id: int,
            message_contents: List[str],
            sender_type: str,
            unix_timestamp: int,
            thread_id: int | None,
        ) -> NewMessageViewModel | None:
            controller_parameters = NewMessageControllerParameters(
                conversation_id=id,
                message_contents=message_contents,
                sender_type=sender_type,
                unix_timestamp=unix_timestamp,
                thread_id=thread_id,
            )

            view_model: NewMessageViewModel = self.execute(
                controller_parameters=controller_parameters,
            )

            return view_model
