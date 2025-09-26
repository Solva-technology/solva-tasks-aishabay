from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.core.code.api.schemas.group import GroupCreate, GroupDB
from services.core.code.core.db import get_async_session
from services.core.code.core.user import role_required
from services.core.code.db.crud.group import group_crud


router = APIRouter()


@router.post("/", response_model=GroupDB)
async def create_new_group(
    new_group: GroupCreate,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(role_required(["admin", "teacher"])),
):
    return await group_crud.create(new_group, session, user)
