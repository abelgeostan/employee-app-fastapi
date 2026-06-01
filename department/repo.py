from datetime import datetime
from sqlite3 import IntegrityError

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import ConflictException
from models.department import Department


async def create(name: str, db: AsyncSession):
    dept = Department(name=name)
    db.add(dept)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(detail=f"Email '{name.strip()}' is already in use")
    await db.refresh(dept)
    return dept


async def get_all(db: AsyncSession) -> list[Department]:
    stmt = select(Department).where(Department.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return result.all()


async def get_by_id(db: AsyncSession, id: int):
    stmt = select(Department).where(Department.id == id)
    result = await db.scalars(stmt)
    return result.first()


async def update(db: AsyncSession, dept: Department):
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(detail=f"Email '{dept.name.strip()}' is already in use")
    await db.refresh(dept)
    return dept


async def delete(db: AsyncSession, dept: Department):
    dept.deleted_at = datetime.now()
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(detail=f"Failed to delete department {dept.id}")
    return dept
