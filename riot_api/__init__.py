"""
Data processing the data from riot API
"""


import os
from riotwatcher import LolWatcher

from dotenv import load_dotenv


from db.db import Session


session = Session()

load_dotenv()
RIOTAPIKEY = os.getenv("RIOT_API_KEY")

watcher = LolWatcher(RIOTAPIKEY)

# pylint: disable=wrong-import-position
from .methods import *
