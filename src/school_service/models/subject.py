"""Subject entity."""

from sqlalchemy import Column, ForeignKey, Identity, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from school_service.models.base import Base

# Association table: which teachers can teach which subjects
subject_teachers = Table(
    "subject_teachers",
    Base.metadata,
    Column("subject_id", Integer, ForeignKey("subject.id"), primary_key=True),
    Column("teacher_id", Integer, ForeignKey("teacher.id"), primary_key=True),
)


class Subject(Base):
    """Subject entity."""

    __tablename__ = "subject"

    id: Mapped[int] = mapped_column(Integer, Identity(always=False), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    timetables: Mapped[list["TimeTable"]] = relationship(
        "TimeTable",
        back_populates="subject",
    )
    teachers: Mapped[list["Teacher"]] = relationship(
        "Teacher",
        secondary=subject_teachers,
        back_populates="subjects",
    )

    def __repr__(self) -> str:
        return f"Subject(id={self.id}, name={self.name!r})"
