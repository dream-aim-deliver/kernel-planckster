from abc import ABC, abstractmethod
from typing import Any, Generic, Literal, Type, TypeVar
from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel, ConfigDict, Field, validator

from lib.core.sdk.presenter import Presentable
from lib.core.sdk.usecase_models import BaseResponse, TBaseErrorResponse, TBaseResponse
from lib.core.sdk.viewmodel import (
    BaseErrorViewModel,
    BaseSuccessViewModel,
    TBaseErrorViewModel,
    TBaseSuccessViewModel,
    TBaseViewModel,
)


class FastAPIFeature(BaseModel):
    name: str
    description: str
    group: str
    verb: Literal["GET", "POST", "PUT", "DELETE"] = "GET"
    endpoint: str
    router: APIRouter | None = None
    presenter: Presentable[BaseSuccessViewModel] | None

    model_config = ConfigDict(arbitrary_types_allowed=True, ignored_types=(Presentable,))

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        group = data["group"]
        name = data["name"]
        # presenter_class = self.presenter_class
        # if presenter_class is not None:
        #     self.presenter: Presentable[BaseSuccessViewModel] = presenter_class()
        self.router: APIRouter = APIRouter(
            prefix=f"/{group}", tags=[group], responses={404: {"description": f"Not found {name}"}}
        )
        self.register_endpoints(self.router)

    @validator("endpoint")
    def endpoint_should_begin_with_slash(cls, v: str) -> str:
        if not v.startswith("/"):
            return f"/{v}"
        return v

    def register_endpoints(self, router: APIRouter) -> None:
        @router.get(f"{self.endpoint}")
        def register_endpoint(request: Request) -> BaseSuccessViewModel | BaseErrorViewModel:
            presenter = self.presenter
            if presenter is None:
                raise HTTPException(status_code=500, detail="Presenter is not defined")
            else:
                view_model: BaseSuccessViewModel = presenter.present_success(
                    response=BaseResponse(status=True, result="Hello World!")
                )
            return self._process_view_model(view_model)

    def _process_view_model(
        self, view_model: BaseSuccessViewModel | BaseErrorViewModel
    ) -> BaseSuccessViewModel | BaseErrorViewModel:
        if isinstance(view_model, BaseSuccessViewModel):
            return view_model
        else:
            raise HTTPException(status_code=view_model.errorCode, detail=view_model)


class BaseDataStructure(BaseModel):
    pass


TBaseDataStructure = TypeVar("TBaseDataStructure", bound=BaseDataStructure)


class TestDataStructure(BaseDataStructure):
    id: int
    name: str


class TestBaseController(ABC, Generic[TBaseDataStructure]):
    def __init__(self, data: TBaseDataStructure) -> None:
        super().__init__()
        self._data = data

    @property
    def data(self) -> TBaseDataStructure:
        return self._data


class TestController(TestBaseController[TestDataStructure]):
    def __init__(self, data: TestDataStructure) -> None:
        super().__init__(data)
        self._id = data.id
        self._name = data.name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name


class SuperController(TestController):
    def __init__(self, description: str, data: TestDataStructure) -> None:
        super().__init__(data)
        self._description = description

    @property
    def description(self) -> str:
        return self._description


class TestBaseFeature(Generic[TBaseDataStructure]):
    def __init__(self, controller: TestBaseController[TBaseDataStructure]) -> None:
        self._controller = controller


TestBaseFeature(SuperController(data=TestDataStructure(id=1, name="test"), description="test"))


class TestSuperFeature(TestBaseFeature[TestDataStructure]):
    def __init__(self, controller: SuperController) -> None:
        super().__init__(controller)


TestSuperFeature(SuperController(data=TestDataStructure(id=1, name="test"), description="test"))
