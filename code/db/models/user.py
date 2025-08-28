from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from code.core.base import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    def __repr__(self):
        return f"id={self.id}, email={self.email}"
