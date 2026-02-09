"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from school_service.config import get_settings
from school_service.database import init_db
from school_service.routers import class_router, subject_router, teacher_router, timetable_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on startup (dev); use Alembic in production."""
    await init_db()
    yield
    # shutdown: close pool etc. if needed


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(class_router.router)
app.include_router(subject_router.router)
app.include_router(teacher_router.router)
app.include_router(timetable_router.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
