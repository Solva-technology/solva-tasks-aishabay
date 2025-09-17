from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.code.api.schemas.user import UserCreate, UserRead
from services.auth.code.core.db import get_async_session
from services.auth.code.core.user import (
    auth_backend,
    current_user,
    fastapi_users,
    role_required,
)
from services.auth.code.db.crud.user import user_crud
from services.auth.code.db.models import User


router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@router.get("/user/me")
async def get_current_user(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    user_id = user.id
    return await user_crud.get_or_404(user_id, session, user)


@router.get("/user/{user_id}")
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(role_required(["admin", "teacher"])),
):
    return await user_crud.get_or_404(user_id, session, user)


@router.get("/user/{user_id}/is_manager")
async def get_manager_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    user = await user_crud.get(user_id, session)
    if not user:
        return {"user_id": user_id, "is_manager": False}

    return {"user_id": user.id, "is_manager": user.role == "manager"}


@router.post("/user/are_students")
async def are_students(
    user_ids: list[int],
    session: AsyncSession = Depends(get_async_session),
):
    user_ids = list(set(user_ids))
    users = await user_crud.get_multi_by_ids(user_ids, session)

    are_students = all(user.role == "student" for user in users)
    return {"user_ids": user_ids, "are_students": are_students}
