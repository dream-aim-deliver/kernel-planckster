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
    client_sub: str | None = Field(title="Client SUB", description="SUB of the new default client.")

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
        default_client_sub: str | None = None,
        default_llm_name: str | None = None,
    ) -> None:
        super().__init__(usecase=usecase, presenter=presenter)
        self.default_client_sub = default_client_sub if default_client_sub is not None else "SDA"
        self.default_llm_name = default_llm_name if default_llm_name is not None else "gpt4"

    def create_request(self, parameters: CreateDefaultDataControllerParameters | None) -> CreateDefaultDataRequest:
        if parameters is None:
            raise HTTPException(status_code=400, detail="Invalid request parameters.")
        else:
            default_client_sub = self.default_client_sub
            default_llm_name = self.default_llm_name

            client_sub = parameters.client_sub if parameters.client_sub is not None else default_client_sub
            llm_name = parameters.llm_name if parameters.llm_name is not None else default_llm_name

            return CreateDefaultDataRequest(client_sub=client_sub, llm_name=llm_name)
