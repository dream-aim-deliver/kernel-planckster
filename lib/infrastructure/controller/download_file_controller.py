from pydantic import Field
from lib.core.entity.models import LFN
from lib.core.sdk.controller import BaseControllerParameters


class DownloadFileControllerParameters(BaseControllerParameters):
    lfn_json: str = Field(
        title="Logical File Name",
        description="The Logical File Name of the file to be downloaded, in JSON format.",
    )
