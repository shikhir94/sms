"""SQLAlchemy models."""

from school_service.models.base import Base
from school_service.models.class_model import SchoolClass
from school_service.models.subject import Subject
from school_service.models.teacher import Teacher
from school_service.models.timetable import TimeTable

__all__ = ["Base", "SchoolClass", "Subject", "Teacher", "TimeTable"]
