from typing import Dict
from fastapi import HTTPException

from pydantic import Field

from lib.core.sdk.controller import BaseController, BaseControllerParameters
from lib.core.usecase.create_default_data_usecase import CreateDefaultDataUseCase
from lib.core.usecase_models.create_default_data_usecase_models import (
    CreateDefaultDataError,
    CreateDefaultDataRequest,
    CreateDefaultDataResponse,
)
from lib.core.view_model.create_default_data_view_model import CreateDefaultDataViewModel
from lib.infrastructure.presenter.create_default_data_presenter import CreateDefaultDataPresenter


class CreateDefaultDataControllerParameters(BaseControllerParameters):
    user_sid: str | None = Field(title="User String ID", description="SID of the new default user.")

    llm_name: str | None = Field(title="LLM Name", description="Name of the new default llm.")


class CreateDefaultDataController(
    BaseController[
        CreateDefaultDataControllerParameters,
        CreateDefaultDataRequest,
        CreateDefaultDataResponse,
        CreateDefaultDataError,
        CreateDefaultDataViewModel,
    ]
):
    def __init__(
        self,
        usecase: CreateDefaultDataUseCase,
        presenter: CreateDefaultDataPresenter,
        default_user_sid: str | None = None,
        default_llm_name: str | None = None,
    ) -> None:
        super().__init__(usecase=usecase, presenter=presenter)
        self.default_user_sid = default_user_sid if default_user_sid is not None else "admin"
        self.default_llm_name = default_llm_name if default_llm_name is not None else "gpt4"

    def create_request(self, parameters: CreateDefaultDataControllerParameters | None) -> CreateDefaultDataRequest:
        if parameters is None:
            raise HTTPException(status_code=400, detail="Invalid request parameters.")
        else:
            default_user_sid = self.default_user_sid
            default_llm_name = self.default_llm_name

            user_sid = parameters.user_sid if parameters.user_sid is not None else default_user_sid
            llm_name = parameters.llm_name if parameters.llm_name is not None else default_llm_name

            return CreateDefaultDataRequest(user_sid=user_sid, llm_name=llm_name)
