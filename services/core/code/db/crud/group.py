import logging

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.core.code.api.schemas.group import GroupCreate
from services.core.code.core.clients import auth_client
from services.core.code.db.crud.base import CRUDBase
from services.core.code.db.models import Group
from services.core.code.db.models.group import GroupStudent


logger = logging.getLogger(__name__)


class CRUDGroup(CRUDBase):
    async def create(
            self,
            obj_in: GroupCreate,
            session: AsyncSession,
            user,
    ):
        logger.info(
            f"Attempting to create {self.model.__name__}",
            extra={
                "user_id": user.get("id", "anonymous"),
                "group_name": obj_in.name,
                "manager_id": obj_in.manager_id,
                "student_ids": obj_in.students,
            },
        )

        if not await auth_client.is_manager(obj_in.manager_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User {obj_in.manager_id} is not a valid manager",
            )

        if (
            obj_in.students and not await auth_client.are_students(
                obj_in.students,
            )
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Some users in {obj_in.students} "
                       f"are not valid students",
            )

        db_obj = self.model(
            name=obj_in.name,
            manager_id=obj_in.manager_id,
        )

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        if obj_in.students:
            for student_id in obj_in.students:
                session.add(
                    GroupStudent(group_fk=db_obj.id, student_fk=student_id),
                )
            await session.commit()

        result = await session.execute(
            select(GroupStudent.student_fk).
            where(GroupStudent.group_fk == db_obj.id),
        )

        student_ids = [row[0] for row in result.fetchall()]

        logger.debug(
            f"Permission granted: user_id={user.get('id')} "
            f"-> {self.model.__name__}.",
        )
        logger.info(
            f"Created {self.model.__name__}(id={db_obj.id}), "
            f"students={student_ids})",
        )

        return db_obj


group_crud = CRUDGroup(Group)
