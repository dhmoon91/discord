"""add columns summoners

Revision ID: f80eab35e57e
Revises: 0be53c6bea83
Create Date: 2021-07-23 05:41:15.899305

"""
from alembic import op
from sqlalchemy import Column, Integer, String

# pylint: skip-file

# revision identifiers, used by Alembic.
revision = "f80eab35e57e"
down_revision = "0be53c6bea83"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("summoners", Column("summoner_icon_image_url", String))
    op.add_column("summoners", Column("summoner_level", Integer))


def downgrade():
    op.drop_column("summoners", "summoner_icon_image_url")
    op.drop_column("summoners", "summoner_level")
