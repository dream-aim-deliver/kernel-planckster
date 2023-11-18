from typing import Annotated, Any

from fastapi import Depends, Request, Response
from lib.core.sdk.fastapi import FastAPIEndpoint
from lib.core.view_model.list_conversations_view_model import ListConversationsViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.list_conversations_controller import ListConversationsControllerParameters

from dependency_injector.wiring import inject, Provide


class ListConversationsFastAPIFeature(
    FastAPIEndpoint[
        ListConversationsControllerParameters, Any, ListConversationsControllerParameters, ListConversationsViewModel
    ]
):
    @inject
    def __init__(
        self,
        descriptor_provider: Any = Provide[ApplicationContainer.list_conversations_feature.feature_descriptor.provider],
        controller_provider: Any = Provide[ApplicationContainer.list_conversations_feature.controller.provider],
    ):
        name = "List Conversations"
        controller = controller_provider()
        descriptor = descriptor_provider()
        responses: dict[int | str, dict[str, Any]] = {
            200: {
                "model": ListConversationsViewModel,
                "description": "Success",
            },
            400: {
                "model": ListConversationsViewModel,
                "description": "Bad Request. Research Context ID does not exist",
            },
            500: {
                "model": ListConversationsViewModel,
                "description": "Internal Server Error",
            },
        }

        super().__init__(name=name, controller=controller, descriptor=descriptor, responses=responses)

    def create_controller_parameters(
        self,
        query: ListConversationsControllerParameters | None,
        body: Any,
    ) -> ListConversationsControllerParameters:
        if query is None:
            return ListConversationsControllerParameters(research_context_id=0)
        else:
            return ListConversationsControllerParameters(research_context_id=query.research_context_id)

    def endpoint_fn(  # type: ignore
        self,
        request: Request,
        response: Response,
        request_query_parameters: Annotated[ListConversationsControllerParameters, Depends()],
    ) -> ListConversationsViewModel | None:
        view_model: ListConversationsViewModel | None = super().endpoint_fn(
            request=request,
            response=response,
            request_query_parameters=request_query_parameters,
        )
        return view_model
