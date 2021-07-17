"""
Data processing the data from riot API
"""


import os
from riotwatcher import LolWatcher
import pandas as pd
import pydash
from dotenv import load_dotenv
from utils.utils import get_file_path

load_dotenv()
RIOTAPIKEY = os.getenv("RIOT_API_KEY")

watcher = LolWatcher(RIOTAPIKEY)
MY_REGION = "na1"

# Get summoner rank.
def get_summoner_rank(name: str):
    """Gets the summoner's rank information from riot watcher api
    Parameters:
    name (str): name of the summoner

    Returns:
    summoner_profile (dict): rank information about the summoner

    """
    # We need to get id
    user = watcher.summoner.by_name(MY_REGION, name)
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
    emblem_path = get_file_path(
        f"ranked-emblems/Emblem_{tier_division.capitalize()}.png"
    )

    summoner_profile = {
        "user_name": user["name"],
        "summoner_icon_image_url": summoner_icon_image_url,
        "summoner_level": user["summonerLevel"],
        "tier_image_path": emblem_path,
        "tier_image_name": f"Emblem_{tier_division.capitalize()}.png",
        "tier": tier,
        "solo_win": solo_win,
        "solo_loss": solo_loss,
        "league_points": league_points,
    }
    return summoner_profile


# Get previous match history of summoner.
def previous_match(name: str):
    """Gets the summoner's last match information from riot watcher api
    Parameters:
    name (str): name of the summoner

    Returns:
    df (DataFrame): summoner's latest match information

    """

    user = watcher.summoner.by_name(MY_REGION, name)
    matches = watcher.match.matchlist_by_account(MY_REGION, user["accountId"])
    last_match = matches["matches"][0]
    match_detail = watcher.match.by_id(MY_REGION, last_match["gameId"])
    # check league's latest version
    latest = watcher.data_dragon.versions_for_region(MY_REGION)["n"]["champion"]
    # Get static info.
    static_champ_list = watcher.data_dragon.champions(latest, False, "en_US")
    # champ static data list.
    champ_dict = {}
    for key in static_champ_list["data"]:
        row = static_champ_list["data"][key]
        champ_dict[row["key"]] = row["id"]

    participants = []
    for row in match_detail["participants"]:
        participants_row = {}
        # Get summoner name
        pid = row["participantId"]
        summoner_info = pydash.find(
            match_detail["participantIdentities"], {"participantId": pid}
        )
        participants_row["Name"] = summoner_info["player"]["summonerName"]
        participants_row["Champion"] = champ_dict[str(row["championId"])]
        # participants_row['spell1'] = row['spell1Id']
        # participants_row['spell2'] = row['spell2Id']
        participants_row["Win"] = row["stats"]["win"]
        participants_row["Kills"] = row["stats"]["kills"]
        participants_row["Deaths"] = row["stats"]["deaths"]
        participants_row["Assists"] = row["stats"]["assists"]
        participants_row["Damage"] = row["stats"]["totalDamageDealt"]
        # participants_row['Gold'] = row['stats']['goldEarned']
        # participants_row['champLevel'] = row['stats']['champLevel']
        # participants_row['Minions'] = row['stats']['totalMinionsKilled']
        # participants_row['item0'] = row['stats']['item0']
        # participants_row['item1'] = row['stats']['item1']
        participants.append(participants_row)
    last_match_info = pd.DataFrame(participants)
    return last_match_info


def create_summoner_list(players_list: list, server_id: str):
    """Gets the list of summoners and returns the information abou the summoners
    Parameters:
    players_list (list): list of summoner names
    server_id (int): discord server id

    Returns:
    members_to_add (dict): summoner's latest match information

    """
    try:
        # dictionary for data input
        members_to_add = {
            server_id: [],
        }

        # accessing each player
        for summoner in players_list:

            user = watcher.summoner.by_name(MY_REGION, summoner)

            user_name = user["name"]

            ranked_stat = watcher.league.by_summoner(MY_REGION, user["id"])

            # get ranked data on summoner
            if len(ranked_stat) > 0:

                solo_rank_stat = pydash.find(
                    ranked_stat, {"queueType": "RANKED_SOLO_5x5"}
                )

                tier_division = solo_rank_stat["tier"]
                tier_rank_number = solo_rank_stat["rank"]
                league_points = solo_rank_stat["leaguePoints"]

            # set the tier to unranked if no ranked data was found
            else:
                tier_division = "UNRANKED"
                tier_rank_number = "I"
                league_points = 0

            members_to_add[server_id].append(
                {
                    "user_name": summoner.replace(" ", ""),
                    "formatted_user_name": user_name,
                    "tier_division": tier_division,
                    "tier_rank_number": tier_rank_number,
                    "league_points": league_points,
                }
            )

        return members_to_add
    # pylint: disable=broad-except
    except Exception as e_str:
        raise Exception(e_str, summoner) from e_str
