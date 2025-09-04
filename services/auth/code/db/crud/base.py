import logging
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.code.db.models import User


logger = logging.getLogger(__name__)


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        logger.debug(f"Fetching {self.model.__name__} with id={obj_id}")
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id),
        )
        obj = db_obj.scalars().first()
        if obj:
            logger.debug(f"Found {self.model.__name__}: {obj}")
        else:
            logger.debug(f"{self.model.__name__} with id={obj_id} not found")
        return obj

    async def get_or_404(
            self,
            obj_id: int,
            session: AsyncSession,
            user: Optional[User],
    ):
        obj = await self.get(obj_id, session)
        if obj is None:
            logger.warning(
                f"{self.model.__name__} with id={obj_id} not found (404)",
            )
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"{self.model.__name__} not found",
            )
        logger.debug(
            f"Access granted: user_id={user.id} -> "
            f"{self.model.__name__}(id={obj_id})",
        )
        return obj

    async def get_owned_or_403(
            self,
            obj_id: int,
            session: AsyncSession,
            user: Optional[User],
            owner_field: str = "author_id",
    ):
        obj = await self.get_or_404(obj_id, session, user)
        if getattr(obj, owner_field) != user.id and not user.is_superuser:
            logger.warning(
                f"Access forbidden: user_id={user.id} "
                f"tried to access {self.model.__name__}(id={obj_id})",
            )
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Not authorized to access this resource",
            )
        logger.debug(
            f"Access granted: user_id={user.id} -> "
            f"{self.model.__name__}(id={obj_id})",
        )
        return obj

    async def get_multi(
        self,
        skip: int,
        limit: int,
        session: AsyncSession,
        user: Optional[User],
    ):
        logger.debug(
            f"Fetching multiple {self.model.__name__} objects "
            f"(skip={skip}, limit={limit})",
        )
        db_objs = await session.execute(
            select(self.model).offset(skip).limit(limit),
        )
        objs = db_objs.scalars().all()
        logger.debug(
            f"Access granted: user_id={user.id} -> "
            f"{self.model.__name__} objects.",
        )
        logger.debug(f"Fetched {len(objs)} {self.model.__name__} objects")
        return objs

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
    ):
        obj_in_data = obj_in.dict()
        logger.info(f"Creating {self.model.__name__} with data={obj_in_data}")
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        logger.info(
            f"Permission granted: user_id={user.id} -> {self.model.__name__}.",
        )
        logger.info(f"Created {self.model.__name__}(id={db_obj.id})")
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None,
    ):
        update_data = obj_in.dict(exclude_unset=True)
        logger.info(
            f"Updating {self.model.__name__}(id={db_obj.id}) "
            f"with {update_data}",
        )
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        logger.debug(
            f"Access granted: user_id={user.id} -> "
            f"{self.model.__name__}(id={db_obj.id})",
        )
        logger.info(f"Updated {self.model.__name__}(id={db_obj.id})")
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
        user: Optional[User] = None,
    ):
        logger.warning(f"Deleting {self.model.__name__}(id={db_obj.id})")
        await session.delete(db_obj)
        await session.commit()
        logger.debug(
            f"Access granted: user_id={user.id} -> "
            f"{self.model.__name__}(id={db_obj.id})",
        )
        logger.warning(f"Deleted {self.model.__name__}(id={db_obj.id})")
        return db_obj
