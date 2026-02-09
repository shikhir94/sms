"""Repository for SchoolClass."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from school_service.models.class_model import SchoolClass


class ClassRepository:
    """CRUD for Class entity."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_all(self) -> list[SchoolClass]:
        result = await self._session.execute(select(SchoolClass))
        return list(result.scalars().all())

    async def save(self, entity: SchoolClass) -> SchoolClass:
        self._session.add(entity)
        await self._session.flush()
        await self._session.refresh(entity)
        return entity
