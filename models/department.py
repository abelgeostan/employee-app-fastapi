from typing import Any

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.employee import _datetime_to_iso
from models.entity import Entity


class Department(Entity):
    __tablename__ = "department"
    __abstract__ = False

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    # created_at: Mapped[datetime] = mapped_column(
    #     DateTime(timezone=True),
    #     server_default=func.now(),
    #     nullable=False,
    # )
    # updated_at: Mapped[datetime | None] = mapped_column(
    #     DateTime(timezone=True),
    #     server_default=func.now(),
    #     onupdate=func.now(),
    #     nullable=True,
    # )
    # deleted_at: Mapped[datetime | None] = mapped_column(
    #     DateTime(timezone=True), nullable=True, default=None
    # )

    employees: Mapped[list["Employee"]] = relationship(  # noqa: F821, UP037
        "Employee",
        secondary="employee_dept",
        back_populates="departments",
    )

    def to_api_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": _datetime_to_iso(self.created_at),
            "updated_at": _datetime_to_iso(self.updated_at),
            "deleted_at": _datetime_to_iso(self.deleted_at),
        }
