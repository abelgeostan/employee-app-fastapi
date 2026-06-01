
from fastapi import FastAPI, Request
import logging
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from dataclasses import dataclass
from typing import TypedDict

from exceptions import NotFoundException
from exceptions.handler import register_exception_handlers
from models.employee import Employee as DBEmployee
from middleware.logger import RequestLoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware

from employees.router import router as employee_router
from auth.router import router as auth_router
from department.router import router as dept_router

from config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await create_tables()
#     yield

app = FastAPI(
    title="Employee CRUD API",
    description="A simple API for managing employee records with dict storage.",
    version="1.0.0",
    # lifespan=lifespan,
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time"],
)


app.include_router(employee_router)
app.include_router(auth_router)
app.include_router(dept_router)

_employees: dict[int, dict] = {}
_next_id: int = 1

register_exception_handlers(app)

def get_next_id() -> int:
    global _next_id
    current_id = _next_id
    _next_id += 1
    return current_id

@dataclass
class EmployeeCreate:
    name:str
    age: int
    designation:str

# Note: ORM model is `DBEmployee` from models.employee; keep local API types minimal

@app.get("/",tags=["Root"])
def root():
    return {"message": "WELCOME TO EMPLOYEE CRUD API"}

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "env": settings.app_env, "debug": settings.debug}


# @app.post("/employee", status_code=status.HTTP_201_CREATED, tags=["Employees"])
# async def create_employee(body: dict = Body(...), db: AsyncSession = Depends(get_db)):
#     name = body.get("name")
#     email = body.get("email")
#     if not isinstance(name, str) or not name.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
#     if not isinstance(email, str) or not email.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
#     db_employee = DBEmployee(name=name.strip(), email=email.strip())
#     db.add(db_employee)
#     try:
#         await db.commit()
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
#     await db.refresh(db_employee)
#     return db_employee.to_api_dict()

# @app.get("/employee", tags=["Employees"])
# async def get_all_employees(db: AsyncSession = Depends(get_db)):
#     stmt = select(DBEmployee).where(DBEmployee.deleted_at.is_(None))
#     result = await db.scalars(stmt)
#     return [r.to_api_dict() for r in result.all()]

# @app.put("/employee/{employee_id}", tags=["Employees"])
# async def update_employee(employee_id: int, body: dict = Body(...), db: AsyncSession = Depends(get_db)):
#     stmt = select(DBEmployee).where(DBEmployee.id == employee_id)
#     result = await db.scalars(stmt)
#     db_employee = result.first()
#     if not db_employee:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee {employee_id} not found")
    
#     if "name" in body and isinstance(body["name"], str) and body["name"].strip():
#         db_employee.name = body["name"].strip()
#     if "email" in body and isinstance(body["email"], str) and body["email"].strip():
#         db_employee.email = body["email"].strip()
    
#     try:
#         await db.commit()
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already in use")
#     await db.refresh(db_employee)
#     return db_employee.to_api_dict()

# @app.get("/employee/{id}", tags=["Employees"])
# async def get_by_id(id: int, db: AsyncSession = Depends(get_db)):
#     stmt = select(DBEmployee).where(DBEmployee.id == id)
#     result = await db.scalars(stmt)
#     db_employee = result.first()
#     if not db_employee:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee {id} not found")
#     return db_employee.to_api_dict()

# @app.delete("/employee/{id}", tags=["Employees"])
# async def delete_by_id(id: int, db: AsyncSession = Depends(get_db)):
#     stmt = select(DBEmployee).where(DBEmployee.id == id)
#     result = await db.scalars(stmt)
#     db_employee = result.first()
#     if not db_employee:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee {id} not found")
#     db_employee.deleted_at = datetime.now()
#     try:
#         await db.commit()
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete employee")
#     return {"message": f"Employee {id} marked as deleted."}
    



    



# @app.put("/employee/{employee_id}", tags=["Employees"])
# def update_employee(employee_id: int, employee: EmployeeCreate):
#     if employee_id not in _employees:
#         return {"error": "Employee not found"}
#     updated_employee = {
#         "id": employee_id,
#         "name": employee.name,
#         "age": employee.age,
#         "designation": employee.designation,
#         # preserve existing deletion state (default to False)
#         "is_deleted": _employees[employee_id].get("is_deleted", False),
#     }
#     _employees[employee_id] = updated_employee
#     return updated_employee

# @app.delete("/employee/{employee_id}", tags=["Employees"])
# def delete_employee(employee_id: int):
#     if employee_id not in _employees or _employees[employee_id].get("is_deleted", False):
#         return {"error": "Employee not found"}
#     _employees[employee_id]["is_deleted"] = True
#     return {"message": f"Employee with id {employee_id} marked as deleted."}






if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
