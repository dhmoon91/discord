"""channels model mapping"""
import datetime
from sqlalchemy import Column, Integer, String, DateTime
from ..db import Base


class Channels(Base):
    """channels model definition"""

    __tablename__ = "channels"

    channel_id = Column(Integer, primary_key=True)
    region = Column(String(20))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
