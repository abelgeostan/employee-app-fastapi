from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_user, require_role
from auth.schemas import TokenPayload
from employees.schemas import (
    AddressResponse,
    EmployeeByIdResponse,
    EmployeeCreate,
    EmployeeResponse,
)
from employees.schemas import EmployeeUpdate
from employees import service
from database.connection import get_db
from models.employee import EmployeeRole


router = APIRouter(prefix="/employee", tags=["Employees"])


"""fix the post"""


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=EmployeeResponse,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def create_employee(body: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    employee = await service.create(db, body)
    return employee


@router.get("/", response_model=list[EmployeeByIdResponse])
async def get_all_employees(
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):

    result = await service.get_all(db)
    return result


@router.put("/{id}", dependencies=[Depends(require_role(EmployeeRole.HR))])
async def update_employee(
    id: int, body: EmployeeUpdate, db: AsyncSession = Depends(get_db)
):
    db_employee = await service.update(db, id, body)
    return db_employee


@router.delete("/{id}", dependencies=[Depends(require_role(EmployeeRole.HR))])
async def delete_by_id(id: int, db: AsyncSession = Depends(get_db)):
    employee = await service.delete(db, id)
    return {"message": f"Employee {id} ({employee.name}) marked as deleted."}


@router.get("/{id}", response_model=EmployeeByIdResponse)
async def get_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    employee = await service.get_by_id(db, id)
    return employee


@router.post("/{emp_id}/departments/{dept_id}")
async def attach_department_to_employee(
    emp_id: int,
    dept_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    employee = await service.attach_department(db, emp_id, dept_id)
    return employee


@router.delete("/{emp_id}/departments/{dept_id}")
async def detach_department_from_employee(
    emp_id: int,
    dept_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    employee = await service.detach_department(db, emp_id, dept_id)
    return employee


@router.delete("/{emp_id}/adresses/{addr_id}", response_model=AddressResponse)
async def delete_address(
    emp_id: int,
    addr_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    address = await service.delete_address(db, emp_id, addr_id)
    return address


"""GET ALL"""

"""do search ....search?name=x .......query param"""
