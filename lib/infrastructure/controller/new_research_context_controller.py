from fastapi import HTTPException
from pydantic import Field
from lib.core.sdk.controller import BaseController, BaseControllerParameters
from lib.core.usecase.new_research_context_usecase import NewResearchContextUseCase
from lib.core.usecase_models.new_research_context_usecase_models import (
    NewResearchContextError,
    NewResearchContextRequest,
    NewResearchContextResponse,
)
from lib.core.view_model.new_research_context_view_mode import NewResearchContextViewModel
from lib.infrastructure.presenter.new_research_context_presenter import NewResearchContextPresenter


class NewResearchContextControllerParameters(BaseControllerParameters):
    research_context_title: str = Field(
        title="Research Context Title",
        description="Title of the research context to be created.",
    )
    research_context_description: str = Field(
        title="Research Context Description",
        description="Description of the research context to be created.",
    )
    client_sub: str = Field(
        title="Client SUB",
        description="SUB of the client for which the research context is to be created.",
    )
    llm_name: str = Field(
        title="LLM Name",
        description="Name of the LLM for which the research context is to be created.",
    )
    source_data_ids: list[int] = Field(
        title="Source Data IDs",
        description="List of source data ids that will be tied to the research context to be created.",
    )
    external_id: str = Field(
        title="External ID",
        description="The UUID that is used to trace vector stores and agents in the externally managed databases.",
    )


class NewResearchContextController(
    BaseController[
        NewResearchContextControllerParameters,
        NewResearchContextRequest,
        NewResearchContextResponse,
        NewResearchContextError,
        NewResearchContextViewModel,
    ]
):
    def __init__(
        self,
        usecase: NewResearchContextUseCase,
        presenter: NewResearchContextPresenter,
    ) -> None:
        super().__init__(usecase=usecase, presenter=presenter)

    def create_request(self, parameters: NewResearchContextControllerParameters | None) -> NewResearchContextRequest:
        if parameters is None:
            raise HTTPException(status_code=400, detail="Invalid request parameters.")
        else:
            return NewResearchContextRequest(
                research_context_title=parameters.research_context_title,
                research_context_description=parameters.research_context_description,
                client_sub=parameters.client_sub,
                llm_name=parameters.llm_name,
                source_data_ids=parameters.source_data_ids,
                external_id=parameters.external_id,
            )
