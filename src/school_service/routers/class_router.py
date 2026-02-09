"""Class API - GET all, POST create (matches Spring ClassController)."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from school_service.database import get_db
from school_service.models.class_model import SchoolClass
from school_service.repositories.class_repository import ClassRepository
from school_service.schemas.class_schema import ClassCreate, ClassRead

router = APIRouter(prefix="/class", tags=["class"])


@router.get("", response_model=list[ClassRead])
async def get_classes(db: AsyncSession = Depends(get_db)) -> list[SchoolClass]:
    repo = ClassRepository(db)
    return await repo.find_all()


@router.post("", response_model=ClassRead)
async def create_class(
    body: ClassCreate,
    db: AsyncSession = Depends(get_db),
) -> SchoolClass:
    repo = ClassRepository(db)
    entity = SchoolClass(name=body.name)
    return await repo.save(entity)
