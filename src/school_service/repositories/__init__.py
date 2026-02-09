"""Data access layer."""

from school_service.repositories.class_repository import ClassRepository
from school_service.repositories.subject_repository import SubjectRepository
from school_service.repositories.teacher_repository import TeacherRepository
from school_service.repositories.timetable_repository import TimeTableRepository

__all__ = [
    "ClassRepository",
    "SubjectRepository",
    "TeacherRepository",
    "TimeTableRepository",
]
