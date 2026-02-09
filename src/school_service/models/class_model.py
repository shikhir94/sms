"""School class entity (table name 'class' to match Spring Boot)."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from school_service.models.base import Base


class SchoolClass(Base):
    """Class entity - maps to table 'class'."""

    __tablename__ = "class"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    timetables: Mapped[list["TimeTable"]] = relationship(
        "TimeTable",
        back_populates="school_class",
        foreign_keys="TimeTable.class_id",
    )

    def __repr__(self) -> str:
        return f"SchoolClass(id={self.id}, name={self.name!r})"
