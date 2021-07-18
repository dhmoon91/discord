"""create summoners table

Revision ID: 09ed5e242c53
Revises: 
Create Date: 2021-07-18 04:43:12.417768

"""
import datetime
from alembic import op
from sqlalchemy import Column, Integer, String, DateTime


# revision identifiers, used by Alembic.
revision = "09ed5e242c53"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "summoners",
        Column("id", Integer, primary_key=True),
        Column("summoner_name", String, nullable=False),
        Column("region", String(20), nullable=False),
        Column("puuid", String, nullable=False, unique=True),
        Column("tier_division", String(10)),
        Column("tier_rank", String(10)),
        Column("solo_win", Integer),
        Column(
            "solo_loss",
            Integer,
        ),
        Column(
            "league_points",
            Integer,
        ),
        Column("created_at", DateTime, default=datetime.datetime.utcnow),
        Column(
            "updated_at",
            DateTime,
            default=datetime.datetime.utcnow,
            onupdate=datetime.datetime.utcnow,
        ),
    )


def downgrade():
    op.drop_table("summoners")
