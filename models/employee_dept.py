from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class employee_dept(Base):
    __tablename__ = "employee_dept"

    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    department_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("department.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
