
from datetime import datetime
from typing import List

from fastapi import HTTPException,status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from employees.schemas import EmployeeCreate
from exceptions import AppException, ConflictException

from models.address import Address
from models.employee import Employee
from sqlalchemy.exc import IntegrityError
import logging
logger=logging.getLogger(__name__)


async def create(db:AsyncSession, employee:Employee)->Employee:
    
    db.add(employee)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException( detail=f"Email '{employee.email.strip()}' is already in use")
    await db.refresh(employee,["addresses","departments"])

    
    
    return employee

async def get_all(db:AsyncSession)->list[Employee]:
    stmt=select(Employee).where(Employee.deleted_at.is_(None)).options(
        selectinload(Employee.departments),
        selectinload(Employee.addresses),
    )
    result = await db.scalars(stmt)
    return result.all()

async def get_by_id(db:AsyncSession,id:int):
    stmt = select(Employee).where(Employee.id == id).options(
        selectinload(Employee.departments),
        selectinload(Employee.addresses),
    )
    result = await db.scalars(stmt)
    return result.first()

async def update(db:AsyncSession, employee: Employee):
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise AppException(detail="Failed to update employee")
    await db.refresh(employee)
    return employee

async def delete(db:AsyncSession,employee:Employee):
    employee.deleted_at = datetime.now()
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise AppException(detail="Failed to delete employee")
    
    return employee


async def get_by_email(db:AsyncSession,email:str)->Employee | None:
    stmt = select(Employee).where(
        Employee.email==email,
        Employee.deleted_at.is_(None),
    )
    result=await db.scalars(stmt)
    return result.first()


async def get_address_by_id(db:AsyncSession, addr_id:int):
    stmt = select(Address).where(
        Address.id==addr_id,
        Address.deleted_at.is_(None),
    )
    result=await db.scalars(stmt)
    return result.first()

async def delete_address(db:AsyncSession, address:Address):
    address.deleted_at = datetime.now()
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise AppException(detail="Failed to delete address")
    return address



