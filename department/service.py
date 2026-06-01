from sqlalchemy.ext.asyncio import AsyncSession
from department import repo
from department.schemas import DeptCreate
from exceptions import NotFoundException


async def create(body: DeptCreate, db: AsyncSession):
    dept = await repo.create(body.name, db)
    return dept


async def get_all(db: AsyncSession):
    result = await repo.get_all(db)
    return result


async def update(db: AsyncSession, id: int, body: DeptCreate):
    dept = await repo.get_by_id(db, id)
    if not dept:
        raise NotFoundException(detail=f"Department {id} not found")
    if body.name is not None and body.name.strip():
        dept.name = body.name.strip()
    dept = await repo.update(db, dept)
    return dept


async def delete(db: AsyncSession, id: int):
    dept = await repo.get_by_id(db, id)
    if not dept:
        raise NotFoundException(detail=f"Department {id} not found")
    dept = await repo.delete(db, dept)
    return dept
