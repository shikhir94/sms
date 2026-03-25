"""Teacher entity."""

from sqlalchemy import Identity, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from school_service.models.base import Base
from school_service.models.subject import subject_teachers


class Teacher(Base):
    """Teacher entity."""

    __tablename__ = "teacher"

    id: Mapped[int] = mapped_column(Integer, Identity(always=False), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    user_name: Mapped[str] = mapped_column(String(255), nullable=False)

    timetables: Mapped[list["TimeTable"]] = relationship(
        "TimeTable",
        back_populates="teacher",
    )
    subjects: Mapped[list["Subject"]] = relationship(
        "Subject",
        secondary=subject_teachers,
        back_populates="teachers",
    )

    def __repr__(self) -> str:
        return f"Teacher(id={self.id}, userName={self.user_name!r})"
