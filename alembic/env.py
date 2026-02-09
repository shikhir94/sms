"""Alembic environment - uses sync PostgreSQL URL from env."""

import os
import sys
from logging.config import fileConfig

# Allow importing school_service when running alembic from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.schema import MetaData

load_dotenv()

# Sync URL for migrations (no asyncpg)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/postgres",
)

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import all models so Base.metadata has them
from school_service.models.base import Base  # noqa: E402

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
