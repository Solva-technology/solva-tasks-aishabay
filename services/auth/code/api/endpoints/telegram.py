from fastapi import APIRouter, Depends
from services.auth.code.api.schemas.user import UserTelegram
from services.auth.code.api.validators import check_user_exists
from services.auth.code.core.db import get_async_session
from services.auth.code.core.user import get_jwt_strategy
from services.auth.code.db.crud.user import user_crud
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.post("/auth/telegram/callback")
async def telegram_auth(
    payload: UserTelegram,
    session: AsyncSession = Depends(get_async_session),
):
    data = payload.dict()
    telegram_id = data["telegram_id"]
    db_user = await check_user_exists(telegram_id, session)

    if not db_user:
        db_user = await user_crud.create(payload, session)

    strategy = get_jwt_strategy()
    token = await strategy.write_token(db_user)

    return {"access_token": token, "token_type": "bearer"}
