"""team_members model mapping"""
import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_json import mutable_json_type

from ..db import Base


class TeamMembers(Base):
    """Team members model definition"""

    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, nullable=False)
    members = Column(mutable_json_type(dbtype=JSONB, nested=True))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    def __init__(
        self,
        channel_id,
        members,
    ):
        self.channel_id = channel_id
        self.members = members
