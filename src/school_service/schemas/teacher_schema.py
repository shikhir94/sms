"""Pydantic schemas for Teacher (matches Spring firstName, lastName, userName)."""

from pydantic import BaseModel, ConfigDict, Field


class TeacherBase(BaseModel):
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    user_name: str = Field(..., alias="userName")

    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
    )


class TeacherCreate(TeacherBase):
    pass


class TeacherRead(TeacherBase):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        serialize_by_alias=True,
    )

    id: int
