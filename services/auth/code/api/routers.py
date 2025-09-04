from fastapi import APIRouter
from services.auth.code.api.endpoints import telegram_router, user_router


main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(telegram_router)
