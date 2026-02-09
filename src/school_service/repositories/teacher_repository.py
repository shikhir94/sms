"""Repository for Teacher."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from school_service.models.teacher import Teacher


class TeacherRepository:
    """CRUD for Teacher entity."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_all(self) -> list[Teacher]:
        result = await self._session.execute(select(Teacher))
        return list(result.scalars().all())

    async def save(self, entity: Teacher) -> Teacher:
        self._session.add(entity)
        await self._session.flush()
        await self._session.refresh(entity)
        return entity
