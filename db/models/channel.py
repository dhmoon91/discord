from sqlalchemy import Column, Integer, String, DateTime
from ..db import Base
import datetime


class Channel(Base):
    __tablename__ = "channels"

    channe_id = Column(Integer, primary_key=True)
    region = Column(String(20))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
