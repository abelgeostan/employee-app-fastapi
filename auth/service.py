

from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import create_access_token, verify_password
# from auth.utils import  create_refresh_token as crt_refresh_token
from exceptions import UnauthorizedException
from employees import repo


async def login(db: AsyncSession, email: str, password: str)-> str:
    employee = await repo.get_by_email(db,email)
    if employee is None:
        raise UnauthorizedException("Invalid email or password")
    if not verify_password(password, employee.password_hash):
        raise UnauthorizedException("Invalid email or password")
    
    return create_access_token({"id": employee.id, "email": employee.email, "role": employee.role.value})

# async def create_refresh_token(db: AsyncSession, email: str)->str:
#     employee = await repo.get_by_email(db,email)
#     if employee is None:
#         raise UnauthorizedException("Invalid email or password")
#     return crt_refresh_token({"id":employee.id, "email":employee.email})