"""create team_members table

Revision ID: 82c39910d8dd
Revises: 09ed5e242c53
Create Date: 2021-07-18 05:15:50.214275

"""
import datetime
from alembic import op
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB

# pylint: skip-file
revision = "82c39910d8dd"
down_revision = "09ed5e242c53"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "team_members",
        Column("id", Integer, primary_key=True),
        Column("channel_id", String, nullable=False),
        Column("members",JSONB),
        Column("created_at", DateTime, default=datetime.datetime.utcnow),
        Column(
            "updated_at",
            DateTime,
            default=datetime.datetime.utcnow,
            onupdate=datetime.datetime.utcnow,
        ),
    )


def downgrade():
    op.drop_table("team_members")
