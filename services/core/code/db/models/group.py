from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.core.code.core.db import Base


class GroupStudent(Base):
    group_fk = mapped_column(ForeignKey("group.id"), primary_key=True)
    student_fk = mapped_column(Integer, primary_key=True)

    id = None


class Group(Base):
    name: Mapped[str] = mapped_column(String, nullable=False)
    manager_id: Mapped[int] = mapped_column(Integer, nullable=False)

    tasks: Mapped[list["Task"]] = relationship(  # noqa: F821
        back_populates="group",
        cascade="all, delete-orphan",
    )

    repr_attrs = (
        "id",
        "name",
        "manager_id",
    )
