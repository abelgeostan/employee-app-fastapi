from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_user
from auth.schemas import TokenPayload
from database.connection import get_db
from department import service
from department.schemas import DeptCreate

router = APIRouter(prefix="/dept", tags=["Departments"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    body: DeptCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    dept = await service.create(body, db)
    return dept


@router.get("/")
async def get_all(
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    result = await service.get_all(db)
    return result


@router.put("/{id}")
async def update(
    id: int,
    body: DeptCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    dept = await service.update(db, id, body)
    return dept


@router.delete("/{id}")
async def delete_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    dept = await service.delete(db, id)
    return {"message": f"Department {id} ({dept.name}) marked as deleted."}
