"""Repository for Subject."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from school_service.models.subject import Subject, subject_teachers
from school_service.models.teacher import Teacher


class SubjectRepository:
    """CRUD for Subject entity."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_all(self) -> list[Subject]:
        result = await self._session.execute(select(Subject))
        return list(result.scalars().all())

    async def find_by_id(self, id: int) -> Subject | None:
        result = await self._session.execute(select(Subject).where(Subject.id == id))
        return result.scalar_one_or_none()

    async def find_teachers_by_subject_id(self, subject_id: int) -> list[Teacher]:
        result = await self._session.execute(
            select(Teacher).join(subject_teachers).where(subject_teachers.c.subject_id == subject_id)
        )
        return list(result.scalars().all())

    async def save(self, entity: Subject) -> Subject:
        self._session.add(entity)
        await self._session.flush()
        await self._session.refresh(entity)
        return entity

    async def delete_by_id(self, id: int) -> None:
        subject = await self.find_by_id(id)
        if subject:
            await self._session.delete(subject)
            await self._session.flush()
