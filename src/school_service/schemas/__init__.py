"""Pydantic request/response schemas."""

from school_service.schemas.class_schema import ClassCreate, ClassRead
from school_service.schemas.subject_schema import SubjectCreate, SubjectRead, SubjectUpdate
from school_service.schemas.teacher_schema import TeacherCreate, TeacherRead
from school_service.schemas.timetable_schema import (
    TimeTableCreate,
    TimeTableRead,
    TimeTableReadDetailed,
)

__all__ = [
    "ClassCreate",
    "ClassRead",
    "SubjectCreate",
    "SubjectRead",
    "SubjectUpdate",
    "TeacherCreate",
    "TeacherRead",
    "TimeTableCreate",
    "TimeTableRead",
    "TimeTableReadDetailed",
]
