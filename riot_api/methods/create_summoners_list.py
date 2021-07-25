import pydash
from db.db import Session
from db.models.summoners import Summoners

from .. import watcher, MY_REGION

session = Session()


def create_summoner_list(players_list: list, server_id: str):
    """Gets the list of summoner names and returns the information abou the summoners
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

            # First check if we have existing record for given summoner name
            # Create query; TODO: check for update_time
            summoner_cached_query = session.query(Summoners).filter(
                Summoners.summoner_name == user["name"]
            )

            # TODO: Retrieve from db.
            # Execute query
            summoner_cached = summoner_cached_query.first()

            if summoner_cached:
                print("summoner found!")
                # summoner_cached = dict(summoner_cached.__dict__)

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

            # TODO create summoner row;
            # profileiconid = user["profileIconId"]
            # version = watcher.data_dragon.versions_for_region(MY_REGION)["v"]

            # summoner_icon_image_url = (
            #     "http://ddragon.leagueoflegends.com/"
            #     + f"cdn/{version}/img/profileicon/{profileiconid}.png"
            # )

            # summoner_data = Summoners(
            #     user["name"],
            #     summoner_icon_image_url,
            #     user["summonerLevel"],
            #     "na1",
            #     user["puuid"],
            #     tier_division,
            #     solo_rank_stat["rank"],
            #     solo_rank_stat["wins"],
            #     solo_rank_stat["losses"],
            #     solo_rank_stat["leaguePoints"],
            # )

            # Create db row.
            # double check if summoner is here?
            # session.add(summoner_data)
            # session.commit()

            members_to_add[server_id].append(
                {
                    "user_name": summoner.replace(" ", ""),
                    "puuid": user["puuid"],
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
