from abc import abstractmethod
from typing import Annotated, Any, Dict, Generic, Literal, Type, TypeVar
from fastapi import APIRouter, Depends, HTTPException, Header, Request, Response
from pydantic import BaseModel, ConfigDict, Field, model_validator, validator
from lib.core.sdk.controller import BaseControllerParameters, TBaseControllerParameters
from lib.core.sdk.feature import BaseFeatureDescriptor

# TODO: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/?h=de#dependency-requirements
# async def verify_auth(x_auth_token: str = Annotated[str, Header()]) -> bool:
#     if x_auth_token != "fake-super-secret-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")
#     return True


class FastAPIFeatureSetRouter:
    def __init__(self, feature_descriptor: BaseFeatureDescriptor) -> None:
        self._feature_descriptor = feature_descriptor
        tags = [self.feature_descriptor.collection]
        # dependencies = []
        if self.feature_descriptor.auth:
            tags.append("auth")
            # dependencies.append(Depends(verify_auth))
        self._fastapi_router = APIRouter(
            prefix=f"/{self.feature_descriptor.collection}",
            tags=tags,  # type: ignore
        )

        self._responses

    @property
    def feature_descriptor(self) -> BaseFeatureDescriptor:
        return self._feature_descriptor

    @property
    def fastapi_router(self) -> APIRouter:
        return self._fastapi_router

    responses: Dict[int | str, dict[str, Any]] | None = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    # @abstractmethod
    # def endpoint_fn(
    #     self,
    #     request: Request,
    #     response: Response,
    #     request_query_parameters: TBaseControllerParameters | None = None,
    #     request_body_parameters: TBaseRequest | None = None,
    # ) -> TBaseViewModel:
    #     raise NotImplementedError("You must implement the endpoint_fn method in your feature")

    # def handle_request(
    #     self,
    #     controller_parameters: TBaseControllerParameters | None = None,
    # ) -> TBaseViewModel:
    #     controller = self.controller_factory()
    #     view_model = controller.execute(controller_parameters)
    #     if view_model is None:
    #         raise HTTPException(
    #             status_code=500,
    #             detail=f"Something went wrong. Controller for {self.verb} {self.endpoint} of feature {self.name} did not produce a view model.",
    #         )
    #     if not view_model.status:
    #         raise HTTPException(status_code=500, detail=view_model)
    #     else:
    #         return view_model

    # def register_endpoints(self, router: APIRouter) -> None:
    #     router.add_api_route(
    #         methods=[self.verb],
    #         tags=[self.group],
    #         path=f"{self.endpoint}",
    #         name=self.name,
    #         description=self.description,
    #         endpoint=self.endpoint_fn,
    #         responses=self.responses,
    #     )
