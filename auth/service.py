from sqlalchemy.ext.asyncio import AsyncSession

from auth import utils
from auth.utils import create_access_token, verify_password
from auth.utils import create_refresh_token as crt_refresh_token
from employees import repo
from exceptions import UnauthorizedException


async def login(db: AsyncSession, email: str, password: str) -> str:
    employee = await repo.get_by_email(db, email)
    if employee is None or employee.deleted_at is not None:
        raise UnauthorizedException("Invalid email or password")
    if not verify_password(password, employee.password_hash):
        raise UnauthorizedException("Invalid email or password")

    return create_access_token(
        {"id": employee.id, "email": employee.email, "role": employee.role.value}
    )


async def create_refresh_token(db: AsyncSession, email: str) -> str:
    employee = await repo.get_by_email(db, email)
    if employee is None:
        raise UnauthorizedException("Invalid email or password")
    return crt_refresh_token(employee.id, employee.email)


async def verify_refresh_token(refresh_token: str):
    payload = utils.decode_access_token(refresh_token)
    return payload


async def create_refresh_access_token(payload: dict, db: AsyncSession):
    employee = await repo.get_by_email(db, payload.get("email"))
    if employee is None or employee.deleted_at is not None:
        raise UnauthorizedException("Invalid email or password")
    return create_access_token(
        {"id": employee.id, "email": employee.email, "role": employee.role.value}
    )
