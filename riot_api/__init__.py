"""
Data processing the data from riot API
"""


import os
from riotwatcher import LolWatcher

from dotenv import load_dotenv
from utils.utils import get_file_path


from db.db import Session


session = Session()

load_dotenv()
RIOTAPIKEY = os.getenv("RIOT_API_KEY")

watcher = LolWatcher(RIOTAPIKEY)
MY_REGION = "na1"
from .methods import *
