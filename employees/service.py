from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import hash_password
from department import repo as deptrepo
from employees import repo
from employees.schemas import AddressCreate, EmployeeCreate, EmployeeUpdate
from exceptions import ConflictException, NotFoundException
from models.address import Address
from models.employee import Employee

"""fix create post"""


async def create(db: AsyncSession, body: EmployeeCreate) -> Employee:

    if not isinstance(body.name, str) or not body.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="name must be a non-empty string",
        )
    if not isinstance(body.email, str) or not body.email.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email must be a non-empty string",
        )

    hashed = hash_password(body.password)
    employee = Employee(
        name=body.name,
        email=body.email,
        password_hash=hashed,
        age=body.age,
        role=body.role,
    )
    if body.address:
        employee.addresses.append(
            Address(
                line1=body.address.line1,
                city=body.address.city,
                postal_code=body.address.postal_code,
                country=body.address.country,
            )
        )
    employee = await repo.create(db, employee)
    return employee


async def get_all(db: AsyncSession):
    result = await repo.get_all(db)
    return result


async def update(db: AsyncSession, id: int, body: EmployeeUpdate):
    db_employee = await repo.get_by_id(db, id)
    if not db_employee:
        raise NotFoundException(detail=f"Employee {id} not found")

    if body.name is not None and body.name.strip():
        db_employee.name = body.name.strip()

    if body.email is not None and body.email.strip():
        db_employee.email = body.email.strip()

    if body.age is not None:
        db_employee.age = body.age

    db_employee = await repo.update(db, db_employee)
    return db_employee


async def delete(db: AsyncSession, id: int):
    db_employee = await repo.get_by_id(db, id)
    if not db_employee:
        raise NotFoundException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee {id} not found"
        )

    db_employee = await repo.delete(db, db_employee)
    return db_employee


async def get_by_id(db: AsyncSession, id: int):

    employee = await repo.get_by_id(db, id)
    if employee is None:
        raise NotFoundException("Employee not found")
    return employee


async def attach_department(db: AsyncSession, emp_id: int, dept_id: int):
    employee = await repo.get_by_id(db, emp_id)
    if not employee:
        raise NotFoundException(detail=f"Employee {emp_id} not found")

    department = await deptrepo.get_by_id(db, dept_id)
    if not department:
        raise NotFoundException(detail=f"Department {dept_id} not found")

    if department not in employee.departments:
        employee.departments.append(department)
        await repo.update(db, employee)

    return employee


async def detach_department(db: AsyncSession, emp_id: int, dept_id: int):
    employee = await repo.get_by_id(db, emp_id)
    if not employee:
        raise NotFoundException(detail=f"Employee {emp_id} not found")

    department = await deptrepo.get_by_id(db, dept_id)
    if not department:
        raise NotFoundException(detail=f"Department {dept_id} not found")

    if department in employee.departments:
        employee.departments.remove(department)
        await repo.update(db, employee)

    return employee


async def delete_address(db: AsyncSession, emp_id: int, addr_id: int):
    employee = await repo.get_by_id(db, emp_id)
    if not employee:
        raise NotFoundException(detail=f"Employee {emp_id} not found")
    address = await repo.get_address_by_id(db, addr_id)
    if not address:
        raise NotFoundException(detail=f"Address {addr_id} not found")
    if address.employee_id != emp_id:
        raise ConflictException(
            detail=f"Address id {addr_id} dont match with employee {emp_id}"
        )
    address = await repo.delete_address(db, address)
    return address


async def search_employees(db: AsyncSession, name: str | None = None):
    employees = await repo.get_all(db)
    if name:
        name = name.strip().lower()
        employees = [emp for emp in employees if name in emp.name.lower()]
    return employees


async def add_address(db: AsyncSession, emp_id: int, addr: AddressCreate):
    employee = await repo.get_by_id(db, emp_id)
    if not employee:
        raise NotFoundException(detail=f"Employee {emp_id} not found")
    address = Address(
        line1=addr.line1,
        city=addr.city,
        postal_code=addr.postal_code,
        country=addr.country,
    )
    employee.addresses.append(address)
    await repo.update(db, employee)
    return employee
