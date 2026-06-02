from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)

from models.employee import EmployeeRole


class AddressCreate(BaseModel):
    line1: str
    city: str
    postal_code: str
    country: str

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Postal code must be a digit value")
        return v

    @model_validator(mode="after")
    def postal_code_length_for_country(self):

        country = self.country.strip().upper()

        n = len(self.postal_code)

        if country in ("US", "USA") and n != 5:
            raise ValueError("US ZIP codes must be exactly 5 digits")

        elif country == "IN" and n != 6:
            raise ValueError("Indian PIN codes must be exactly 6 digits")

        return self


class EmployeeCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(min_length=1)
    email: EmailStr
    age: int | None = Field(ge=0, le=150)
    address: AddressCreate | None
    password: str = Field(min_length=6)
    role: EmployeeRole = EmployeeRole.DEVELOPER


class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class AddressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    line1: str
    city: str
    postal_code: str
    country: str


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    age: int | None
    role: EmployeeRole

    departments: list[DepartmentResponse] = []
    addresses: list[AddressResponse] = []


class EmployeeByIdResponse(EmployeeResponse):
    created_at: datetime
    updated_at: datetime


class EmployeeUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    age: int | None = Field(None, ge=0, le=150)


"""create other schemaas and update router"""
