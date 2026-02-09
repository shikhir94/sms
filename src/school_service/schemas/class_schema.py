"""Pydantic schemas for Class (SchoolClass)."""

from pydantic import BaseModel, ConfigDict


class ClassBase(BaseModel):
    name: str


class ClassCreate(ClassBase):
    pass


class ClassRead(ClassBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
