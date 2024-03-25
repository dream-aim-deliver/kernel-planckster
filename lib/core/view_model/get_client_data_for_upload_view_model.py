from pydantic import Field
from lib.core.sdk.viewmodel import BaseViewModel


class GetClientDataForUploadViewModel(BaseViewModel):
    """
    View Model for the Get Client Data For Upload Feature.
    """

    signed_url: str = Field(description="The signed URL to upload the file.")

    model_config = {"json_schema_extra": {"examples": [{"status": True, "signed_url": "auth1_string"}]}}
