"""TimeTable API - GET all, GET by class/teacher, POST create."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from school_service.database import get_db
from school_service.models.timetable import TimeTable
from school_service.repositories.timetable_repository import TimeTableRepository
from school_service.schemas.timetable_schema import (
    ConflictItem,
    HasConflictsRequest,
    HasConflictsResponse,
    TimeTableCreate,
    TimeTableRead,
    TimeTableReadDetailed,
)

router = APIRouter(prefix="/timetable", tags=["timetable"])


@router.get("", response_model=list[TimeTableReadDetailed])
async def find_all(db: AsyncSession = Depends(get_db)) -> list[TimeTable]:
    repo = TimeTableRepository(db)
    return await repo.find_all_with_relations()


@router.get("/findByClass/{class_id}", response_model=list[TimeTableReadDetailed])
async def findBy_class(
    class_id: int,
    db: AsyncSession = Depends(get_db),
) -> list[TimeTable]:
    repo = TimeTableRepository(db)
    return await repo.find_by_class_id_with_relations(class_id)


@router.get("/findByTeacher/{teacher_id}", response_model=list[TimeTableReadDetailed])
async def findBy_teacher(
    teacher_id: int,
    db: AsyncSession = Depends(get_db),
) -> list[TimeTable]:
    repo = TimeTableRepository(db)
    return await repo.find_by_teacher_id_with_relations(teacher_id)


DAY_NAMES = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday"}


@router.post("/hasConflicts", response_model=HasConflictsResponse)
async def has_conflicts(
    body: HasConflictsRequest,
    db: AsyncSession = Depends(get_db),
) -> HasConflictsResponse:
    """Check if assigning teacher/subject to slots would cause teacher double-booking."""
    repo = TimeTableRepository(db)
    slots = [(t.day, t.period) for t in body.times]
    existing = await repo.find_by_teacher_at_slots(body.teacher_id, slots)
    conflicts = [
        ConflictItem(
            message=f"Teacher {t.teacher.first_name} {t.teacher.last_name} already assigned to Class {t.school_class.name} on {DAY_NAMES.get(t.day, f'Day {t.day}')}, Period {t.period}"
        )
        for t in existing
    ]
    return HasConflictsResponse(has_conflicts=len(conflicts) > 0, conflicts=conflicts)


@router.post("", response_model=TimeTableRead)
async def create(
    body: TimeTableCreate,
    db: AsyncSession = Depends(get_db),
) -> TimeTable:
    repo = TimeTableRepository(db)
    entity = TimeTable(
        day=body.day,
        period=body.period,
        class_id=body.class_id,
        teacher_id=body.teacher_id,
        subject_id=body.subject_id,
    )
    return await repo.save(entity)
