"""
Data processing the data from riot API
"""
import pydash
from db.models.summoners import Summoners
from db.utils import check_cached
from utils.utils import get_file_path

from .. import watcher


def create_summoner_profile_data(summoner: dict):
    """
    Helper to create data to be returned fro 'get_rank()' function
    """
    emblem_path = get_file_path(
        f"images/Emblem_{summoner['tier_division'].capitalize()}.png"
    )

    tier = " ".join([summoner["tier_division"], summoner["tier_rank"]])

    summoner_profile = {
        "summoner_name": summoner["summoner_name"],
        "summoner_icon_image_url": summoner["summoner_icon_image_url"],
        "summoner_level": summoner["summoner_level"],
        "tier_image_path": emblem_path,
        "tier_image_name": f"Emblem_{summoner['tier_division'].capitalize()}.png",
        "tier": tier,
        "puuid": summoner["puuid"],
        "tier_division": summoner["tier_division"],
        "tier_rank": summoner["tier_rank"],
        "solo_win": summoner["solo_win"],
        "solo_loss": summoner["solo_loss"],
        "league_points": summoner["league_points"],
    }

    return summoner_profile


# Get summoner rank.
def get_summoner_rank(name: str, region: str):
    """Gets the summoner's rank information from riot watcher api
    Parameters:
    name (str): name of the summoner

    Returns:
    summoner_profile (dict): rank information about the summoner

    """

    # We need to get id
    user = watcher.summoner.by_name(region, name)
    print(user)
    # First check if we have existing record for given summoner name
    summoner_cached = check_cached(user["name"], Summoners, Summoners.summoner_name)

    # If data exists, form data and return here.
    if summoner_cached:
        return create_summoner_profile_data(summoner_cached["dict"])

    # Cached value doesn't exist; Grab data from API.
    ranked_stat = watcher.league.by_summoner(region, user["id"])

    # Init 'profile_data' to contain all data needed in one place.
    profile_data = {}

    # Format keys and save into 'profile_data'
    profile_data["summoner_name"] = user["name"]
    profile_data["summoner_level"] = user["summonerLevel"]
    profile_data["puuid"] = user["puuid"]

    # Get summoner Icon Image
    profileiconid = user["profileIconId"]

    version = watcher.data_dragon.versions_for_region(region)["v"]
    profile_data["summoner_icon_image_url"] = (
        "http://ddragon.leagueoflegends.com/"
        + f"cdn/{version}/img/profileicon/{profileiconid}.png"
    )

    # Find solo queue data.
    solo_rank_stat = pydash.find(ranked_stat, {"queueType": "RANKED_SOLO_5x5"})
    if solo_rank_stat:
        profile_data["tier_division"] = solo_rank_stat["tier"]
        profile_data["tier_rank"] = solo_rank_stat["rank"]
        profile_data["solo_win"] = solo_rank_stat["wins"]
        profile_data["solo_loss"] = solo_rank_stat["losses"]
        profile_data["league_points"] = solo_rank_stat["leaguePoints"]

    # If summoner does not have any rank information
    else:
        profile_data["tier_division"] = "UNRANKED"
        profile_data["tier_rank"] = "I"
        profile_data["solo_win"] = 0
        profile_data["solo_loss"] = 0
        profile_data["league_points"] = 0

    summoner_profile = create_summoner_profile_data(profile_data)

    summoner_data = Summoners(summoner_profile)
    summoner_data.create()

    return summoner_profile
