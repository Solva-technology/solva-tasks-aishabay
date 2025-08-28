from fastapi import APIRouter

from code.api.endpoints import user_router


main_router = APIRouter()

main_router.include_router(user_router)
