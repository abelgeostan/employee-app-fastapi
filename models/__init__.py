"""ORM entities."""

from models.address import Address
from models.department import Department
from models.employee import Employee
from models.employee_dept import employee_dept
from models.entity import Entity

__all__ = ["Employee", "Entity", "Address", "Department", "employee_dept"]
