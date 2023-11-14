from abc import ABC, abstractmethod
from typing import Any, Generic, List, Literal, Type, TypeVar
from fastapi import APIRouter, FastAPI, Request, Response
from pydantic import BaseModel, ConfigDict


class FastAPIFeature(BaseModel):
    name: str
    description: str
    base: str
    verb: Literal["GET", "POST", "PUT", "DELETE"] = "GET"
    endpoint: str
    router: APIRouter | None = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        base = data["base"]
        name = data["name"]
        self.router: APIRouter = APIRouter(
            prefix=f"/{base}", tags=[base], responses={404: {"description": f"Not found {name}"}}
        )
        self.register_endpoints(self.router)

    def register_endpoints(self, router: APIRouter) -> None:
        @router.get("/endpoint")
        def register_endpoint(request: Request) -> Response:
            return Response(f"Hello World from {self.name}'s {self.base} route collection!")


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
