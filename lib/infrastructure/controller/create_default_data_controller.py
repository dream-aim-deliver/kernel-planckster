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
    user_sid: str = Field(name="User String ID", description="SID of the new default user.")

    llm_name: str = Field(name="LLM Name", description="Name of the new default llm.")


class CreateDefaultDataController(
    BaseController[
        CreateDefaultDataControllerParameters,
        CreateDefaultDataRequest,
        CreateDefaultDataResponse,
        CreateDefaultDataError,
        CreateDefaultDataViewModel,
    ]
):
    def __init__(self, usecase: CreateDefaultDataUseCase, presenter: CreateDefaultDataPresenter) -> None:
        super().__init__(usecase=usecase, presenter=presenter)

    def create_request(self, parameters: CreateDefaultDataControllerParameters | None) -> CreateDefaultDataRequest:
        if parameters is None:
            raise HTTPException(status_code=400, detail="Invalid request parameters.")
        else:
            return CreateDefaultDataRequest(user_sid=parameters.user_sid, llm_name=parameters.llm_name)
