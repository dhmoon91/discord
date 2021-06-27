import os
from riotwatcher import LolWatcher, ApiError
import pandas as pd
import pydash

from dotenv import load_dotenv

load_dotenv()
RIOTAPIKEY = os.getenv("RIOT_API_KEY")

watcher = LolWatcher(RIOTAPIKEY)
my_region = "na1"

# Get summoner rank.
def getSummonerRank(name: str):
    # We need to get id
    user = watcher.summoner.by_name(my_region, name)
    ranked_stat = watcher.league.by_summoner(my_region, user["id"])

    # Find solo queue data.
    solo_rank_stat = pydash.find(ranked_stat, {"queueType": "RANKED_SOLO_5x5"})

    return " ".join([solo_rank_stat["tier"], solo_rank_stat["rank"]])


# Get previous match history of summoner.
def previousMatch(name: str):
    user = watcher.summoner.by_name(my_region, name)
    matches = watcher.match.matchlist_by_account(my_region, user["accountId"])
    last_match = matches["matches"][0]
    match_detail = watcher.match.by_id(my_region, last_match["gameId"])
    print("teatea")
    # check league's latest version
    latest = watcher.data_dragon.versions_for_region(my_region)["n"]["champion"]
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
        summonerInfo = pydash.find(
            match_detail["participantIdentities"], {"participantId": pid}
        )
        participants_row["Name"] = summonerInfo["player"]["summonerName"]
        participants_row["Champion"] = champ_dict[str(row["championId"])]
        # participants_row['spell1'] = row['spell1Id']
        # participants_row['spell2'] = row['spell2Id']
        participants_row["Win"] = row["stats"]["win"]
        participants_row["Kills"] = row["stats"]["kills"]
        participants_row["Deaths"] = row["stats"]["deaths"]
        participants_row["Assists"] = row["stats"]["assists"]
        participants_row["Damage"] = row["stats"]["totalDamageDealt"]
        participants_row["Gold"] = row["stats"]["goldEarned"]
        # participants_row['champLevel'] = row['stats']['champLevel']
        participants_row["Minions"] = row["stats"]["totalMinionsKilled"]
        # participants_row['item0'] = row['stats']['item0']
        # participants_row['item1'] = row['stats']['item1']
        participants.append(participants_row)
    df = pd.DataFrame(participants)
    return df
