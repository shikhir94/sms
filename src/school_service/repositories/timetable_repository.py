"""Repository for TimeTable."""

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from school_service.models.timetable import TimeTable


def _timetable_with_relations():
    """Query options to eager-load class, teacher, subject (ManyToOne)."""
    return select(TimeTable).options(
        selectinload(TimeTable.school_class),
        selectinload(TimeTable.teacher),
        selectinload(TimeTable.subject),
    )


class TimeTableRepository:
    """CRUD for TimeTable entity."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_all(self) -> list[TimeTable]:
        result = await self._session.execute(select(TimeTable))
        return list(result.scalars().all())

    async def find_all_with_relations(self) -> list[TimeTable]:
        result = await self._session.execute(_timetable_with_relations())
        return list(result.unique().scalars().all())

    async def find_by_class_id(self, class_id: int) -> list[TimeTable]:
        result = await self._session.execute(
            select(TimeTable).where(TimeTable.class_id == class_id)
        )
        return list(result.scalars().all())

    async def find_by_class_id_with_relations(self, class_id: int) -> list[TimeTable]:
        result = await self._session.execute(
            _timetable_with_relations().where(TimeTable.class_id == class_id)
        )
        return list(result.unique().scalars().all())

    async def find_by_teacher_id(self, teacher_id: int) -> list[TimeTable]:
        result = await self._session.execute(
            select(TimeTable).where(TimeTable.teacher_id == teacher_id)
        )
        return list(result.scalars().all())

    async def find_by_teacher_id_with_relations(
        self, teacher_id: int
    ) -> list[TimeTable]:
        result = await self._session.execute(
            _timetable_with_relations().where(TimeTable.teacher_id == teacher_id)
        )
        return list(result.unique().scalars().all())

    async def find_by_teacher_at_slots(
        self, teacher_id: int, slots: list[tuple[int, int]]
    ) -> list[TimeTable]:
        """Find existing timetable entries where teacher is assigned at any (day, period)."""
        if not slots:
            return []
        conditions = [
            (TimeTable.day == day) & (TimeTable.period == period)
            for day, period in slots
        ]
        stmt = (
            select(TimeTable)
            .where(TimeTable.teacher_id == teacher_id)
            .where(or_(*conditions))
            .options(
            selectinload(TimeTable.school_class),
            selectinload(TimeTable.teacher),
        )
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def save(self, entity: TimeTable) -> TimeTable:
        self._session.add(entity)
        await self._session.flush()
        await self._session.refresh(entity)
        return entity
