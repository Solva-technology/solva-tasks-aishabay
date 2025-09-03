from http import HTTPStatus
from typing import Optional, Union

from fastapi import Depends, HTTPException, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from code.api.schemas.user import UserCreate
from code.core.config import settings
from code.core.constants import JWT_LIFETIME_SECONDS, PASSWORD_MAX_LEN
from code.core.db import get_async_session
from code.db.models import User


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET_WORD,
        lifetime_seconds=JWT_LIFETIME_SECONDS,
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager):
    async def validate_password(
        self, password: str, user: Union[UserCreate, User],
    ) -> None:
        if len(password) <= PASSWORD_MAX_LEN:
            raise InvalidPasswordException(
                reason=f"The password should contain more "
                       f"than {PASSWORD_MAX_LEN} characters.",
            )

        if user.email in password:
            raise InvalidPasswordException(
                reason="The password should NOT contain the email",
            )

    async def on_after_register(
            self, user: User,
            request: Optional[Request] = None,
    ):
        pass


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)


def role_required(roles: list[str]):
    async def wrapper(user: User = Depends(current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user
    return wrapper
