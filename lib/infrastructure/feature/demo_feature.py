from typing import Annotated, Any, Dict, Literal, Type

from fastapi import Depends, Request, Response

from lib.core.sdk.feature import BaseFeatureSetDescriptor


class DemoFastAPIFeatureSet:
    def __init__(self, descriptor: BaseFeatureSetDescriptor) -> None:
        pass

    # def endpoint_fn(  # type: ignore
    #     self,
    #     request: Request,
    #     response: Response,
    #     request_query_parameters: Annotated[DemoControllerParameters, Depends()],
    #     # request_body_parameters: DemoControllerParameters,
    # ) -> DemoViewModel:
    #     # Make controller parameters here with your FastAPI request parameters
    #     controllerParameters: DemoControllerParameters = request_query_parameters
    #     return self.handle_request(
    #         controller_parameters=controllerParameters,
    #     )
