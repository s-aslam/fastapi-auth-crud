from fastapi import APIRouter

from project.items.api import router as item_router
from project.user.api import router as user_router

root_api_router = APIRouter()
root_api_router.include_router(user_router, tags=["User"])
root_api_router.include_router(item_router, prefix='/item', tags=["Items"])
