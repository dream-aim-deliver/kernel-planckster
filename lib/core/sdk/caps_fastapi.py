from abc import ABC, abstractmethod
from typing import Any, Generic, Literal, TypeVar
from fastapi import APIRouter, Request, Response
from pydantic import BaseModel, ConfigDict, validator

from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase_models import TBaseErrorResponse, TBaseResponse
from lib.core.sdk.viewmodel import TBaseViewModel


class FastAPIFeature(BaseModel, Generic[TBaseResponse, TBaseErrorResponse, TBaseViewModel]):
    name: str
    description: str
    group: str
    verb: Literal["GET", "POST", "PUT", "DELETE"] = "GET"
    endpoint: str
    router: APIRouter | None = None
    presenter_class: type[BasePresenter[TBaseResponse, TBaseErrorResponse, TBaseViewModel]] | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        group = data["group"]
        name = data["name"]
        presenter_class = self.presenter_class
        if presenter_class is not None:
            self.presenter: BasePresenter[TBaseResponse, TBaseErrorResponse, TBaseViewModel] = presenter_class()
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
        def register_endpoint(request: Request) -> Response:
            # take view model from presenter and return a response instead
            return Response(f"Hello World from {self.name}'s {self.group} route collection!")

    # def _process_view_model(self, view_model: TBaseViewModel) -> Response:
    #     if(view_model.status):
    #         return Response(f"Hello World from {self.name}'s {self.group} route collection!")
    #     return
    #         HTTPException(
    #             status_code=404,
    #             detail=f"Item {item_id} not found",
    #         )


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
