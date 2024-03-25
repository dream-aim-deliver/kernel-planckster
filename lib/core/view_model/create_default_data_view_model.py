from pydantic import Field
from lib.core.sdk.viewmodel import BaseViewModel


class CreateDefaultDataViewModel(BaseViewModel):
    """
    View Model for the Create Default Data Feature. Represents a new default client and a new default llm.
    """

    client_id: int = Field(description="Client id of the new default client.")
    llm_id: int = Field(description="LLM id of the new default llm.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "client_id": 1,
                    "llm_id": 1,
                }
            ]
        }
    }
