"""team_members model mapping"""
from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_json import mutable_json_type
from ..db import Base
from .base import BaseMixin


class TeamMembers(BaseMixin, Base):
    """Team members model definition"""

    __tablename__ = "team_members"

    channel_id = Column(Integer, nullable=False)
    members = Column(mutable_json_type(dbtype=JSONB, nested=True))

    def __init__(
        self,
        channel_id,
        members,
    ):
        super().__init__()
        self.channel_id = channel_id
        self.members = members
