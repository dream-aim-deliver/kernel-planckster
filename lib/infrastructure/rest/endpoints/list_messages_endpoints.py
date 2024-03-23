from typing import Any
from dependency_injector.wiring import inject, Provide

from lib.core.sdk.fastapi import FastAPIEndpoint
from lib.core.view_model.list_messages_view_model import ListMessagesViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.list_messages_controller import ListMessagesControllerParameters


class ListMessagesFastAPIFeature(FastAPIEndpoint[ListMessagesControllerParameters, ListMessagesViewModel]):
    @inject
    def __init__(
        self,
        descriptor: Any = Provide[ApplicationContainer.list_messages_feature.feature_descriptor],
        controller: Any = Provide[ApplicationContainer.list_messages_feature.controller],
    ):
        responses: dict[int | str, dict[str, Any]] = {
            200: {
                "model": ListMessagesViewModel,
                "description": "Success",
            },
            400: {
                "model": ListMessagesViewModel,
                "description": "Bad Request.",
            },
            500: {
                "model": ListMessagesViewModel,
                "description": "Internal Server Error",
            },
        }

        super().__init__(controller=controller, descriptor=descriptor, responses=responses)

    def register_endpoint(self) -> None:
        @self.router.get(
            name=self.name,
            description=self.descriptor.description,
            path="/conversations/{conversation_id}/messages",
            responses=self.responses,
        )
        def endpoint(
            conversation_id: int,
        ) -> ListMessagesViewModel | None:
            controller_parameters = ListMessagesControllerParameters(
                conversation_id=conversation_id,
            )

            view_model: ListMessagesViewModel = self.execute(
                controller_parameters=controller_parameters,
            )

            return view_model
