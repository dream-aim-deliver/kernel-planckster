from typing import List
from fastapi import HTTPException

from pydantic import Field
from lib.core.sdk.controller import BaseController, BaseControllerParameters
from lib.core.usecase.new_source_data_usecase import NewSourceDataUseCase
from lib.core.usecase_models.new_source_data_usecase_models import (
    NewSourceDataError,
    NewSourceDataRequest,
    NewSourceDataResponse,
)
from lib.core.view_model.new_source_data_view_model import NewSourceDataViewModel
from lib.infrastructure.presenter.new_source_data_presenter import NewSourceDataPresenter


class NewSourceDataControllerParameters(BaseControllerParameters):
    knowledge_source_id: int = Field(
        name="Knowledge Source ID", description="Research context id for which the source data is to be registered."
    )
    source_data_lfn_list: List[str] = Field(
        name="List of LFNs", description="List of LFNs of the source data to be registered."
    )


class NewSourceDataController(
    BaseController[
        NewSourceDataControllerParameters,
        NewSourceDataRequest,
        NewSourceDataResponse,
        NewSourceDataError,
        NewSourceDataViewModel,
    ]
):
    def __init__(self, usecase: NewSourceDataUseCase, presenter: NewSourceDataPresenter) -> None:
        super().__init__(usecase=usecase, presenter=presenter)

    def create_request(self, parameters: NewSourceDataControllerParameters | None) -> NewSourceDataRequest:
        if parameters is None:
            raise HTTPException(status_code=400, detail="Invalid request parameters.")
        else:
            return NewSourceDataRequest(
                knowledge_source_id=parameters.knowledge_source_id, source_data_lfn_list=parameters.source_data_lfn_list
            )
