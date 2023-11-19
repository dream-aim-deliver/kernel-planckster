from lib.core.sdk.viewmodel import BaseViewModel


class NewSourceDataViewModel(BaseViewModel):
    """
    View Model for the New Source Data Feature.
    """

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": True,
                },
            ]
        }
    }
