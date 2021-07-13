from sqlalchemy import Column, Integer, String, DateTime
from ..db import Base
import datetime


class Summoners(Base):
    __tablename__ = "summoners"

    id = Column(Integer, primary_key=True)
    channel_id = Column(String)
    region = Column(String(20))
    puuid = Column(String)
    tier_division = Column(String(10))
    tier_rank = Column(String(10))
    solo_win = Column(Integer)
    solo_loss = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    def __init__(
        self, channel_id, region, puuid, tier_division, tier_rank, solo_win, solo_loss
    ):
        self.channel_id = channel_id
        self.region = region
        self.puuid = puuid
        self.tier_division = tier_division
        self.tier_rank = tier_rank
        self.solo_win = solo_win
        self.solo_loss = solo_loss
