from typing import Optional

from fastapi_users import schemas
from services.auth.code.core.enum import UserRole
from pydantic import BaseModel, EmailStr


class UserRead(schemas.BaseUser[int]):
    telegram_id: Optional[int]
    username: Optional[str] = None
    full_name: Optional[str]
    role: Optional[UserRole]


class UserCreate(schemas.BaseUserCreate):
    telegram_id: Optional[int]
    username: Optional[str] = None
    full_name: Optional[str]
    role: Optional[UserRole]


class UserUpdate(schemas.BaseUserUpdate):
    telegram_id: Optional[int]
    username: Optional[str] = None
    full_name: Optional[str]
    role: Optional[UserRole]


class UserTelegram(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]
    telegram_id: Optional[int]
    username: Optional[str] = None
    full_name: Optional[str]
    role: Optional[UserRole]
