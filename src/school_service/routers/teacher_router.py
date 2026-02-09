"""Teacher API - GET all, POST create (matches Spring TeacherController)."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from school_service.database import get_db
from school_service.models.teacher import Teacher
from school_service.repositories.teacher_repository import TeacherRepository
from school_service.schemas.teacher_schema import TeacherCreate, TeacherRead

router = APIRouter(prefix="/teacher", tags=["teacher"])


@router.get("", response_model=list[TeacherRead])
async def get_teachers(db: AsyncSession = Depends(get_db)) -> list[Teacher]:
    repo = TeacherRepository(db)
    return await repo.find_all()


@router.post("", response_model=TeacherRead)
async def create_teacher(
    body: TeacherCreate,
    db: AsyncSession = Depends(get_db),
) -> Teacher:
    repo = TeacherRepository(db)
    entity = Teacher(
        first_name=body.first_name,
        last_name=body.last_name,
        user_name=body.user_name,
    )
    return await repo.save(entity)
