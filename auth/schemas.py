from pydantic import BaseModel

from models.employee import EmployeeRole


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenPayload(BaseModel):
    """Decoded JWT payload."""

    id: int
    email: str
    role: EmployeeRole
