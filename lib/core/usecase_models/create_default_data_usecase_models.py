from typing import Dict, List
from pydantic import Field
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest, BaseResponse


class CreateDefaultDataRequest(BaseRequest):
    """
    Request Model for the Create Default Data Use Case.
    """

    user_sid: str = Field(description="SID of the new default user.")
    llm_name: str = Field(description="Name of the new default llm.")


class CreateDefaultDataResponse(BaseResponse):
    """
    Response Model for the Create Default Data Use Case.
    """

    knowledge_sources_dict: Dict[str, int] = Field(
        description="Dictionary of knowledge source enum names as keys, values as ids in the database of the new default knowledge sources. There should be one default knowledge source in the database per KnowledgeSourceEnum member."
    )
    user_id: int = Field(description="User id of the new default user.")
    llm_id: int = Field(description="LLM id of the new default llm.")


class CreateDefaultDataError(BaseErrorResponse):
    """
    Error Response Model for the Create Default Data Use Case.
    """

    pass
