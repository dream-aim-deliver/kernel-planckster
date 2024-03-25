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
    client_id: int = Field(
        title="Knowledge Source ID", description="Research context id for which the source data is to be registered."
    )
    source_data_name: str = Field(
        title="Source Data Name",
        description="Name of the source data to be registered. Should be something meaningful that can be shown to end users.",
    )
    protocol: str = Field(
        title="Protocol",
        description="The protocol used to access the source data.",
    )
    relative_path: str = Field(
        title="Relative Path",
        description="The relative path to the source data.",
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
                client_id=parameters.client_id,
                source_data_name=parameters.source_data_name,
                protocol=parameters.protocol,
                relative_path=parameters.relative_path,
            )
