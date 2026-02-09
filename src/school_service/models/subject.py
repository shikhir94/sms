"""Subject entity."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from school_service.models.base import Base


class Subject(Base):
    """Subject entity."""

    __tablename__ = "subject"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    timetables: Mapped[list["TimeTable"]] = relationship(
        "TimeTable",
        back_populates="subject",
    )

    def __repr__(self) -> str:
        return f"Subject(id={self.id}, name={self.name!r})"
