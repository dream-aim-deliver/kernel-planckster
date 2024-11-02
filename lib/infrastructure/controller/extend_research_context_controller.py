from fastapi import HTTPException
from pydantic import Field
from lib.core.sdk.controller import BaseController, BaseControllerParameters
from lib.core.usecase.extend_research_context_usecase import ExtendResearchContextUseCase
from lib.core.usecase_models.extend_research_context_usecase_models import (
    ExtendResearchContextError,
    ExtendResearchContextRequest,
    ExtendResearchContextResponse,
)
from lib.core.view_model.extend_research_context_view_model import ExtendResearchContextViewModel
from lib.infrastructure.presenter.extend_research_context_presenter import ExtendResearchContextPresenter


class ExtendResearchContextControllerParameters(BaseControllerParameters):
    new_research_context_title: str = Field(
        title="Research Context Title",
        description="Title of the new research context to be created to include new data sources.",
    )
    new_research_context_description: str = Field(
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
    new_source_data_ids: list[int] = Field(
        title="Source Data IDs",
        description="List of additional source data ids beyond those in the original research context.",
    )
    existing_research_context_id: int = Field(
        title="Existing Research Context ID",
        description="ID of the existing research context to be extended.",
    )
    external_id: str = Field(
        title="External ID",
        description="The UUID that is used to trace vector stores and agents in the externally managed databases.",
    )


class ExtendResearchContextController(
    BaseController[
        ExtendResearchContextControllerParameters,
        ExtendResearchContextRequest,
        ExtendResearchContextResponse,
        ExtendResearchContextError,
        ExtendResearchContextViewModel,
    ]
):
    def __init__(
        self,
        usecase: ExtendResearchContextUseCase,
        presenter: ExtendResearchContextPresenter,
    ) -> None:
        super().__init__(usecase=usecase, presenter=presenter)

    def create_request(
        self, parameters: ExtendResearchContextControllerParameters | None
    ) -> ExtendResearchContextRequest:
        if parameters is None:
            raise HTTPException(status_code=400, detail="Invalid request parameters.")
        else:
            return ExtendResearchContextRequest(
                new_research_context_title=parameters.new_research_context_title,
                new_research_context_description=parameters.new_research_context_description,
                client_sub=parameters.client_sub,
                llm_name=parameters.llm_name,
                new_source_data_ids=parameters.new_source_data_ids,
                existing_research_context_id=parameters.existing_research_context_id,
                external_id=parameters.external_id,
            )
