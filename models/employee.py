"""
Employee entity — ORM mapped class for table `employees`.
"""

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import DateTime, Enum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


import enum
from models.entity import Entity
# from models.address import address


def _datetime_to_iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()

class EmployeeRole(str, enum.Enum):
    UI = "UI"
    UX = "UX"
    DEVELOPER="Developer"
    HR = "HR"

class Employee(Entity):
    __tablename__ = "employees"
    __abstract__=False

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    addresses: Mapped[list["Address"]] = relationship(
        "Address",
        back_populates="employee",
    )

    departments: Mapped[list["Department"]] = relationship(
        "Department",
        secondary="employee_dept",
        back_populates="employees",
    )

    role: Mapped[EmployeeRole] = mapped_column(
        Enum(EmployeeRole, name="employeerole",values_callable=lambda enum_cls: [e.value for e in enum_cls]),
        nullable=False,
        server_default=EmployeeRole.DEVELOPER.value,
    )

    def to_api_dict(self) -> dict[str, Any]:
        """JSON-friendly representation (ISO 8601 for timestamps)."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "created_at": _datetime_to_iso(self.created_at),
            "updated_at": _datetime_to_iso(self.updated_at),
            "deleted_at": _datetime_to_iso(self.deleted_at),
        }