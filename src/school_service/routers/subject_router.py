"""Subject API - full CRUD (matches Spring SubjectController)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from school_service.database import get_db
from school_service.models.subject import Subject
from school_service.repositories.subject_repository import SubjectRepository
from school_service.schemas.subject_schema import SubjectCreate, SubjectRead, SubjectUpdate
from school_service.schemas.teacher_schema import TeacherRead

router = APIRouter(prefix="/subject", tags=["subject"])


@router.get("", response_model=list[SubjectRead])
async def find_all(db: AsyncSession = Depends(get_db)) -> list[Subject]:
    repo = SubjectRepository(db)
    return await repo.find_all()


@router.get("/{subject_id}/teachers", response_model=list[TeacherRead])
async def find_teachers_by_subject(
    subject_id: int,
    db: AsyncSession = Depends(get_db),
) -> list:
    repo = SubjectRepository(db)
    subject = await repo.find_by_id(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    teachers = await repo.find_teachers_by_subject_id(subject_id)
    return teachers


@router.get("/{id}", response_model=SubjectRead)
async def find(id: int, db: AsyncSession = Depends(get_db)) -> Subject:
    repo = SubjectRepository(db)
    subject = await repo.find_by_id(id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject


@router.post("", response_model=SubjectRead)
async def create(
    body: SubjectCreate,
    db: AsyncSession = Depends(get_db),
) -> Subject:
    repo = SubjectRepository(db)
    entity = Subject(name=body.name)
    return await repo.save(entity)


@router.put("", response_model=SubjectRead)
async def update(
    body: SubjectUpdate,
    db: AsyncSession = Depends(get_db),
) -> Subject:
    repo = SubjectRepository(db)
    subject = await repo.find_by_id(body.id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    subject.name = body.name
    return await repo.save(subject)