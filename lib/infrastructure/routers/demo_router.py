from fastapi import APIRouter
from lib.core.view_model.demo_view_model import DemoViewModel
from dependency_injector.wiring import inject, Provide

router = APIRouter()


@inject
@router.get("/")
async def index() -> str:
    return "Hello, world!"
