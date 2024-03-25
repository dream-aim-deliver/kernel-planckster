from pydantic import Field
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest, BaseResponse


class CreateDefaultDataRequest(BaseRequest):
    """
    Request Model for the Create Default Data Use Case.
    """

    client_sub: str = Field(description="SUB of the new default client.")
    llm_name: str = Field(description="Name of the new default llm.")


class CreateDefaultDataResponse(BaseResponse):
    """
    Response Model for the Create Default Data Use Case.
    """

    client_id: int = Field(description="Client ID of the new default client.")
    llm_id: int = Field(description="LLM ID of the new default llm.")


class CreateDefaultDataError(BaseErrorResponse):
    """
    Error Response Model for the Create Default Data Use Case.
    """

    pass
