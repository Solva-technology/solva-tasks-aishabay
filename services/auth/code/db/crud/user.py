import logging
from typing import Optional

from fastapi_users.password import PasswordHelper
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.code.db.crud.base import CRUDBase
from services.auth.code.db.models import User


logger = logging.getLogger(__name__)

password_helper = PasswordHelper()


class CRUDUser(CRUDBase):
    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
    ):
        obj_in_data = obj_in.dict()
        obj_in_data["hashed_password"] = password_helper.hash(
            obj_in_data.pop("password"),
        )
        logger.info(f"Creating {self.model.__name__} with data={obj_in_data}")
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        if user:
            logger.info(
                f"Permission granted: user_id={user.id} -> "
                f"{self.model.__name__}.",
            )
        logger.info(f"Created {self.model.__name__}(id={db_obj.id})")
        return db_obj

    async def get_by_telegram_id(
            self,
            telegram_id: int,
            session: AsyncSession,
    ):
        logger.debug(
            f"Fetching {self.model.__name__} with "
            f"telegram_id={telegram_id}",
        )
        db_obj = await session.execute(
            select(self.model).where(self.model.telegram_id == telegram_id),
        )
        obj = db_obj.scalars().first()
        if obj:
            logger.debug(f"Found {self.model.__name__}: {obj}")
        else:
            logger.debug(
                f"{self.model.__name__} with "
                f"telegram_id={telegram_id} not found",
            )
        return obj


user_crud = CRUDUser(User)
