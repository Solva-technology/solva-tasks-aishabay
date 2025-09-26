from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.core.code.core.db import Base
from services.core.code.core.enum import TaskStatus


class Task(Base):
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(String, nullable=False)

    student_id: Mapped[int] = mapped_column(Integer, nullable=False)

    group_id: Mapped[int] = mapped_column(
        ForeignKey("group.id", ondelete="CASCADE"),
        nullable=False,
    )
    group: Mapped["Group"] = relationship(  # noqa: F821
        back_populates="tasks",
        passive_deletes=True,
    )

    deadline: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    repr_attrs = (
        "id",
        "title",
        "status",
        "student_id",
        "group_id",
        "deadline",
    )
