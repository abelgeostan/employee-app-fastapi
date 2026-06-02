from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_user
from auth.schemas import TokenPayload
from database.connection import get_db
from department import service
from department.schemas import DeptCreate, DeptResponse, DeptResponseById

router = APIRouter(prefix="/dept", tags=["Departments"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=DeptResponse)
async def create(
    body: DeptCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    dept = await service.create(body, db)
    return dept


@router.get("/", response_model=list[DeptResponse])
async def get_all(
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    result = await service.get_all(db)
    return result


@router.get("/{id}", response_model=DeptResponseById)
async def get_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    dept = await service.get_by_id(db, id)
    return dept


@router.put("/{id}", response_model=DeptResponseById)
async def update(
    id: int,
    body: DeptCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    dept = await service.update(db, id, body)
    return dept


@router.delete("/{id}", response_model=DeptResponseById)
async def delete_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    dept = await service.delete(db, id)
    return {"message": f"Department {id} ({dept.name}) marked as deleted."}
