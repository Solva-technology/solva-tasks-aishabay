from fastapi import APIRouter

from services.core.code.api.endpoints import group_router


main_router = APIRouter()

main_router.include_router(
    group_router,
    prefix="/group",
    tags=["Group"],
)
