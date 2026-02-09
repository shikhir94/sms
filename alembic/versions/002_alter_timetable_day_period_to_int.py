"""Alter timetable: day and period from string to integer.

Revision ID: 002
Revises: 001
Create Date: 2025-02-05

Run: alembic upgrade head

If your table is named "time_table" (not "timetable"), edit op.alter_column
to use the correct table name below.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Use "time_table" or "timetable" to match your actual Postgres table name
TABLE_NAME = "time_table"


def upgrade() -> None:
    op.alter_column(
        TABLE_NAME,
        "day",
        existing_type=sa.String(255),
        type_=sa.Integer(),
        postgresql_using="day::integer",
    )
    op.alter_column(
        TABLE_NAME,
        "period",
        existing_type=sa.String(255),
        type_=sa.Integer(),
        postgresql_using="period::integer",
    )


def downgrade() -> None:
    op.alter_column(
        TABLE_NAME,
        "day",
        existing_type=sa.Integer(),
        type_=sa.String(255),
        postgresql_using="day::text",
    )
    op.alter_column(
        TABLE_NAME,
        "period",
        existing_type=sa.Integer(),
        type_=sa.String(255),
        postgresql_using="period::text",
    )
