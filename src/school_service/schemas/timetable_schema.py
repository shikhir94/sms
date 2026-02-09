"""Pydantic schemas for TimeTable."""

from pydantic import BaseModel, ConfigDict, Field

from school_service.schemas.class_schema import ClassRead
from school_service.schemas.subject_schema import SubjectRead
from school_service.schemas.teacher_schema import TeacherRead


class TimeTableBase(BaseModel):
    day: int
    period: int
    class_id: int
    teacher_id: int
    subject_id: int


class TimeTableCreate(TimeTableBase):
    pass


class TimeTableRead(TimeTableBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TimeSlot(BaseModel):
    """Day and period (both 1-based)."""

    day: int
    period: int


class HasConflictsRequest(BaseModel):
    """Request to check if assigning teacher/subject to slots would cause conflicts."""

    class_id: int = Field(..., alias="classId")
    teacher_id: int = Field(..., alias="teacherId")
    subject_id: int = Field(..., alias="subjectId")
    times: list[TimeSlot]

    model_config = ConfigDict(populate_by_name=True)


class ConflictItem(BaseModel):
    """Single conflict with human-readable message."""

    message: str


class HasConflictsResponse(BaseModel):
    """Whether assigning would cause teacher double-booking at any slot."""

    has_conflicts: bool = Field(..., alias="hasConflicts")
    conflicts: list[ConflictItem] = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True, serialize_by_alias=True)


class TimeTableReadDetailed(BaseModel):
    """TimeTable with nested class, teacher, subject (like JPA @ManyToOne)."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        serialize_by_alias=True,
    )

    id: int
    day: int
    period: int
    school_class: ClassRead = Field(..., alias="class")
    teacher: TeacherRead
    subject: SubjectRead
