from datetime import datetime

from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str
    manager_id: int
    students: list[int]


class GroupRequest(BaseModel):
    name: str
    manager_id: int


class GroupUpdate(BaseModel):
    name: str
    manager_id: int
    students: list[int]


class GroupDB(GroupRequest):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
