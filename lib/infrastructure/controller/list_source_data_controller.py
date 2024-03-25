from fastapi import HTTPException
from pydantic import Field
from lib.core.sdk.controller import BaseController, BaseControllerParameters
from lib.core.usecase.list_source_data_usecase import ListSourceDataUseCase
from lib.core.usecase_models.list_source_data_usecase_models import (
    ListSourceDataError,
    ListSourceDataRequest,
    ListSourceDataResponse,
)
from lib.core.view_model.list_source_data_view_model import ListSourceDataViewModel
from lib.infrastructure.presenter.list_source_data_presenter import ListSourceDataPresenter


class ListSourceDataControllerParameter(BaseControllerParameters):
    client_id: int = Field(
        title="Client ID",
        description="Client ID for which the source data is to be listed.",
    )


class ListSourceDataController(
    BaseController[
        ListSourceDataControllerParameter,
        ListSourceDataRequest,
        ListSourceDataResponse,
        ListSourceDataError,
        ListSourceDataViewModel,
    ]
):
    def __init__(self, usecase: ListSourceDataUseCase, presenter: ListSourceDataPresenter) -> None:
        super().__init__(usecase=usecase, presenter=presenter)

    def create_request(self, parameters: ListSourceDataControllerParameter | None) -> ListSourceDataRequest:
        if parameters is None:
            raise HTTPException(status_code=400, detail="Invalid request parameters.")
        else:
            return ListSourceDataRequest(client_id=parameters.client_id)
