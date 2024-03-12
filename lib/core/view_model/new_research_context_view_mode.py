from pydantic import Field
from lib.core.sdk.viewmodel import BaseViewModel


class NewResearchContextViewModel(BaseViewModel):
    """
    View Model for the New Research Context Feature.
    """

    research_context_id: int = Field(description="ID of the newly created research context.")
    research_context_title: str = Field(description="Title of the newly created research context.")
    research_context_description: str = Field(description="Description of the newly created research context.")
    llm_name: str = Field(description="Name of the LLM of the newly created research context.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "research_context_id": 1,
                    "research_context_title": "My Super Cool Research Context",
                    "llm_name": "llama2",
                }
            ]
        }
    }
