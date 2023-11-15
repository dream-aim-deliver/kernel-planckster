from pydantic import Field
from lib.core.sdk.viewmodel import BaseViewModel


class DemoViewModel(BaseViewModel):
    sum: int = Field(description="Sum of the numbers")
