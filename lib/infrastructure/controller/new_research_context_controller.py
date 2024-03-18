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
    user_sid: str | None = Field(
        title="User String ID",
        description="SID of the user for which the research context is to be created.",
    )
    llm_name: str | None = Field(
        title="LLM Name",
        description="Name of the LLM for which the research context is to be created.",
    )
    source_data_ids: list[int] = Field(
        title="Source Data IDs",
        description="List of source data ids that will be tied to the research context to be created.",
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
        default_user_sid: str | None = None,
        default_llm_name: str | None = None,
    ) -> None:
        super().__init__(usecase=usecase, presenter=presenter)

        # NOTE: this are put here for the sake of the demo
        self.default_user_sid = default_user_sid if default_user_sid is not None else "admin"

        self.default_llm_name = default_llm_name if default_llm_name is not None else "gpt4"

    def create_request(self, parameters: NewResearchContextControllerParameters | None) -> NewResearchContextRequest:
        if parameters is None:
            raise HTTPException(status_code=400, detail="Invalid request parameters.")
        else:
            default_user_sid = self.default_user_sid
            default_llm_name = self.default_llm_name

            research_context_title = parameters.research_context_title

            research_context_description = parameters.research_context_description

            user_sid = parameters.user_sid if parameters.user_sid is not None else default_user_sid
            llm_name = parameters.llm_name if parameters.llm_name is not None else default_llm_name
            source_data_ids = parameters.source_data_ids

            return NewResearchContextRequest(
                research_context_title=research_context_title,
                research_context_description=research_context_description,
                user_sid=user_sid,
                llm_name=llm_name,
                source_data_ids=source_data_ids,
            )
