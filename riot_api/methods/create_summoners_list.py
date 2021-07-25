from .get_rank import get_summoner_rank


def create_summoner_list(user_input_list_names: list, server_id: str):
    """Gets the list of summoner names and returns the information abou the summoners
    Parameters:
    players_list (list): list of summoner names
    server_id (int): discord server id

    Returns:
    members_to_add (dict): summoner's latest match information

    """
    try:
        # dictionary for data input
        members_to_add = []

        # accessing each player
        for user_input_list_name in user_input_list_names:
            # 'get_summoner_rank' will handle getting summoner's data.
            summoner_data = get_summoner_rank(user_input_list_name)

            members_to_add.append(
                {
                    "puuid": summoner_data["puuid"],
                    "summoner_name": summoner_data["summoner_name"],
                    "tier_division": summoner_data["tier_division"],
                    "tier_rank": summoner_data["tier_rank"],
                    "league_points": summoner_data["league_points"],
                }
            )
        return members_to_add
    # pylint: disable=broad-except
    except Exception as e_str:
        raise Exception(e_str, user_input_list_name) from e_str
