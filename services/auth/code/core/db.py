from datetime import datetime

from sqlalchemy import DateTime, func, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import (
    declarative_base,
    declared_attr,
    Mapped,
    mapped_column,
    sessionmaker,
)

from services.auth.code.core.config import settings


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # noqa: A003

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    repr_attrs: tuple[str, ...] = ("id",)

    def __repr__(self):
        values = ", ".join(
            f"{attr}={getattr(self, attr)}"
            for attr in self.repr_attrs
            if hasattr(self, attr)
        )
        return f"<{self.__class__.__name__}({values})>"


Base = declarative_base(cls=PreBase)

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=not settings.PRODUCTION,
    future=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False,
)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
