from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from libs.common.enums import UserRole
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from code.core.base import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    telegram_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, index=True, nullable=False,
    )
    username: Mapped[str | None] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(String, nullable=False)

    def __repr__(self):
        return (
            f"id={self.id}, "
            f"telegram_id={self.telegram_id}, "
            f"email={self.email}"
        )
