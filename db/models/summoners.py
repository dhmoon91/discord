"""
summoners model mapping

"""
from sqlalchemy import Column, Integer, String
from ..db import Base
from .base import BaseMixin


class Summoners(BaseMixin, Base):
    """summoners model definition"""

    __tablename__ = "summoners"

    summoner_name = Column(String)
    summoner_icon_image_url = Column(String)
    summoner_level = Column(Integer)
    region = Column(String(20))
    puuid = Column(String)
    tier_division = Column(String(10))
    tier_rank = Column(String(10))
    solo_win = Column(Integer)
    solo_loss = Column(Integer)
    league_points = Column(Integer)

    def __init__(self, summoner_data):
        super().__init__()
        self.summoner_name = summoner_data["summoner_name"]
        self.summoner_icon_image_url = (summoner_data["summoner_icon_image_url"],)
        self.summoner_level = (summoner_data["summoner_level"],)
        self.region = ("na1",)
        self.puuid = (summoner_data["puuid"],)
        self.tier_division = (summoner_data["tier_division"],)
        self.tier_rank = (summoner_data["tier_rank"],)
        self.solo_win = (summoner_data["solo_win"],)
        self.solo_loss = (summoner_data["solo_loss"],)
        self.league_points = (summoner_data["league_points"],)
