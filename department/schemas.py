from datetime import datetime

from pydantic import BaseModel


class DeptCreate(BaseModel):
    name: str


class DeptResponse(BaseModel):
    id: int
    name: str


class DeptResponseById(DeptResponse):
    created_at: datetime
    updated_at: datetime
