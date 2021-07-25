"""
Data processing the data from riot API
"""
import pydash
from db.db import Session
from db.models.summoners import Summoners

from utils.utils import get_file_path

from .. import watcher, MY_REGION


session = Session()

# Get summoner rank.
def get_summoner_rank(name: str):
    """Gets the summoner's rank information from riot watcher api
    Parameters:
    name (str): name of the summoner

    Returns:
    summoner_profile (dict): rank information about the summoner

    """
    # TODO BEFORE REQUESTING DATA, CHECK DB AND UPDATE_TIME TO SEE IF WE ALREADY HAVE DATA.
    # IF WE HAVE DATA BUT UPDATE_TIME IS OVER THE CONSTRAINT, WE SHOULD DELETE THE ROW.

    # We need to get id
    user = watcher.summoner.by_name(MY_REGION, name)

    # First check if we have existing record for given summoner name
    # Create query; TODO: check for update_time
    summoner_cached_query = session.query(Summoners).filter(
        Summoners.summoner_name == user["name"]
    )

    # Execute query
    summoner_cached = summoner_cached_query.one_or_none()

    # If data exists, form data and return here.
    if summoner_cached:
        summoner_cached = dict(summoner_cached.__dict__)
        tier = " ".join(
            [summoner_cached["tier_division"], summoner_cached["tier_rank"]]
        )

        emblem_path = get_file_path(
            f"images/Emblem_{summoner_cached['tier_division'].capitalize()}.png"
        )

        summoner_profile = {
            "user_name": summoner_cached["summoner_name"],
            "summoner_icon_image_url": summoner_cached["summoner_icon_image_url"],
            "summoner_level": summoner_cached["summoner_level"],
            "tier_image_path": emblem_path,
            "tier_image_name": f"Emblem_{summoner_cached['tier_division'].capitalize()}.png",
            "tier": tier,
            "puuid": summoner_cached["puuid"],
            "tier_division": summoner_cached["tier_division"],
            "tier_rank": summoner_cached["tier_rank"],
            "solo_win": summoner_cached["solo_win"],
            "solo_loss": summoner_cached["solo_loss"],
            "league_points": summoner_cached["league_points"],
        }

        return summoner_profile
    # Cached value doesn't exist; Grab data from API.
    ranked_stat = watcher.league.by_summoner(MY_REGION, user["id"])

    # Get summoner Icon Image
    profileiconid = user["profileIconId"]
    version = watcher.data_dragon.versions_for_region(MY_REGION)["v"]
    summoner_icon_image_url = (
        "http://ddragon.leagueoflegends.com/"
        + f"cdn/{version}/img/profileicon/{profileiconid}.png"
    )

    # Find solo queue data.
    if len(ranked_stat) > 0:
        solo_rank_stat = pydash.find(ranked_stat, {"queueType": "RANKED_SOLO_5x5"})
        tier_division = solo_rank_stat["tier"]
        tier_rank = solo_rank_stat["rank"]
        solo_win = solo_rank_stat["wins"]
        solo_loss = solo_rank_stat["losses"]
        league_points = solo_rank_stat["leaguePoints"]

    # If summoner does not have any rank information
    else:
        tier_division = "UNRANKED"
        tier_rank = "I"
        solo_win = 0
        solo_loss = 0
        league_points = 0

    tier = " ".join([tier_division, tier_rank])

    # Get aboslute path to emblem file.
    emblem_path = get_file_path(f"images/Emblem_{tier_division.capitalize()}.png")

    summoner_profile = {
        "user_name": user["name"],
        "summoner_icon_image_url": summoner_icon_image_url,
        "summoner_level": user["summonerLevel"],
        "tier_image_path": emblem_path,
        "tier_image_name": f"Emblem_{tier_division.capitalize()}.png",
        "tier": tier,
        "puuid": user["puuid"],
        "tier_division": tier_division,
        "tier_rank": tier_rank,
        "solo_win": solo_win,
        "solo_loss": solo_loss,
        "league_points": league_points,
    }

    summoner_data = Summoners(
        summoner_profile["user_name"],
        summoner_icon_image_url,
        user["summonerLevel"],
        "na1",
        summoner_profile["puuid"],
        summoner_profile["tier_division"],
        summoner_profile["tier_rank"],
        summoner_profile["solo_win"],
        summoner_profile["solo_loss"],
        summoner_profile["league_points"],
    )

    # Create db row.
    session.add(summoner_data)
    session.commit()

    return summoner_profile
