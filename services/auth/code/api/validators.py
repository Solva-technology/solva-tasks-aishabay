from services.auth.code.db.crud.user import user_crud
from sqlalchemy.ext.asyncio import AsyncSession


async def check_user_exists(
    telegram_id: int,
    session: AsyncSession,
):
    return await user_crud.get_by_telegram_id(telegram_id, session)
