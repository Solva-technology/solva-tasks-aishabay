from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from services.auth.code.core.base import Base
from services.auth.code.core.enum import UserRole


class User(SQLAlchemyBaseUserTable[int], Base):
    telegram_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, index=True, nullable=False,
    )
    username: Mapped[str | None] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(String, nullable=False)

    repr_attrs = (
        "id",
        "telegram_id",
        "email",
        "full_name",
        "role",
    )
