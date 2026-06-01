from pydantic import BaseModel


class DeptCreate(BaseModel):
    name: str
