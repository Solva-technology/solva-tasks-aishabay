from fastapi import APIRouter

from code.api.schemas.user import UserCreate, UserRead, UserUpdate
from code.core.user import auth_backend, fastapi_users


router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/telegram/callback",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth/telegram/callback",
    tags=["auth"],
)

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)

users_router.routes = [
    rout for rout in users_router.routes if rout.name != "users:delete_user"
]

router.include_router(
    users_router,
    prefix="/users",
    tags=["users"],
)
