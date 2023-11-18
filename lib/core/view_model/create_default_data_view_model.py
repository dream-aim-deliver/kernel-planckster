from typing import Dict
from pydantic import Field
from lib.core.sdk.viewmodel import BaseViewModel


class CreateDefaultDataViewModel(BaseViewModel):
    """
    View Model for the Create Default Data Feature. Represents a new default user and a new default llm.
    """

    knowledge_sources_dict: Dict[str, int] = Field(
        description="Dictionary of knowledge source enum names as keys, values as ids in the database of the new default knowledge sources. There should be one default knowledge source in the database per KnowledgeSourceEnum member."
    )
    user_id: int = Field(description="User id of the new default user.")
    llm_id: int = Field(description="LLM id of the new default llm.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "knowledge_sources_dict": {
                        "TELEGRAM": 1,
                        "TWITTER": 2,
                    },
                    "user_id": 1,
                    "llm_id": 1,
                }
            ]
        }
    }
