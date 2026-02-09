"""Teacher entity."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from school_service.models.base import Base


class Teacher(Base):
    """Teacher entity."""

    __tablename__ = "teacher"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    user_name: Mapped[str] = mapped_column(String(255), nullable=False)

    timetables: Mapped[list["TimeTable"]] = relationship(
        "TimeTable",
        back_populates="teacher",
    )

    def __repr__(self) -> str:
        return f"Teacher(id={self.id}, userName={self.user_name!r})"
