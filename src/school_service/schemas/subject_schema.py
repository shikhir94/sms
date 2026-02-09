"""Pydantic schemas for Subject."""

from pydantic import BaseModel, ConfigDict


class SubjectBase(BaseModel):
    name: str


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(SubjectBase):
    id: int


class SubjectRead(SubjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
