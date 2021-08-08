"""channels model mapping"""
from sqlalchemy import Column, Integer, String
from ..db import Base
from .base import BaseMixin


class Channels(BaseMixin, Base):
    """channels model definition"""

    __tablename__ = "channels"

    channel_id = Column(Integer, unique=True)
    region = Column(String(20))

    def __init__(
        self,
        channel_id,
        region,
    ):
        super().__init__()
        self.channel_id = channel_id
        self.region = region
