"""TimeTable entity with ManyToOne to Class, Teacher, Subject."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Identity, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from school_service.models.base import Base

if TYPE_CHECKING:
    from school_service.models.class_model import SchoolClass
    from school_service.models.subject import Subject
    from school_service.models.teacher import Teacher


class TimeTable(Base):
    """TimeTable entity - day, period, and references to class, teacher, subject."""

    __tablename__ = "time_table"

    id: Mapped[int] = mapped_column(Integer, Identity(always=False), primary_key=True)
    day: Mapped[int] = mapped_column(Integer, nullable=False)
    period: Mapped[int] = mapped_column(Integer, nullable=False)
    class_id: Mapped[int] = mapped_column(
        ForeignKey("class.id"),
        nullable=False,
    )
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teacher.id"),
        nullable=False,
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subject.id"),
        nullable=False,
    )

    school_class: Mapped["SchoolClass"] = relationship(
        "SchoolClass",
        back_populates="timetables",
        foreign_keys=[class_id],
    )
    teacher: Mapped["Teacher"] = relationship(
        "Teacher",
        back_populates="timetables",
    )
    subject: Mapped["Subject"] = relationship(
        "Subject",
        back_populates="timetables",
    )

    def __repr__(self) -> str:
        return (
            f"TimeTable(id={self.id}, day={self.day!r}, period={self.period!r})"
        )
