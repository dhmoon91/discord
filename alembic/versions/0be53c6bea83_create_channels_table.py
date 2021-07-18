"""create channels table

Revision ID: 0be53c6bea83
Revises: 82c39910d8dd
Create Date: 2021-07-18 05:24:14.633494

"""
# pylint: disable-all
import datetime
from alembic import op
from sqlalchemy import Column, Integer, String, DateTime


# revision identifiers, used by Alembic.
revision = "0be53c6bea83"
down_revision = "82c39910d8dd"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "channels",
        Column("id", Integer, primary_key=True),
        Column("channel_id", String, nullable=False, unique=True),
        Column("region", String(20), nullable=False),
        Column("created_at", DateTime, default=datetime.datetime.utcnow),
        Column(
            "updated_at",
            DateTime,
            default=datetime.datetime.utcnow,
            onupdate=datetime.datetime.utcnow,
        ),
    )


def downgrade():
    op.drop_table("channels")
