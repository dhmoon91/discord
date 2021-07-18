"""
summoners model mapping

"""
import datetime
from sqlalchemy import Column, Integer, String, DateTime
from ..db import Base


class Summoners(Base):
    """summoners model definition"""

    __tablename__ = "summoners"

    id = Column(Integer, primary_key=True)
    summoner_name = Column(String)
    region = Column(String(20))
    puuid = Column(String)
    tier_division = Column(String(10))
    tier_rank = Column(String(10))
    solo_win = Column(Integer)
    solo_loss = Column(Integer)
    league_points = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    def __init__(
        self,
        summoner_name,
        region,
        puuid,
        tier_division,
        tier_rank,
        solo_win,
        solo_loss,
        league_points,
    ):
        self.summoner_name = summoner_name
        self.region = region
        self.puuid = puuid
        self.tier_division = tier_division
        self.tier_rank = tier_rank
        self.solo_win = solo_win
        self.solo_loss = solo_loss
        self.league_points = league_points
