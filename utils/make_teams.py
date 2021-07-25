from .constants import TIER_VALUE, RANK_VALUE, UNCOMMON_TIERS


def make_teams(list_of_summoners: dict):
    """Gets the list of summoners and returns makes two teams
    Parameters:
    list_of_summoners (dict): list of summoners

    Returns:
    team_blue (dict): 1st team with 5 members
    team_red (dict): 2nd team with 5 members

    """

    for summoner in list_of_summoners:

        # since tier rank numbers for unranked, master, gm and challengers
        # are automatically set to I but we need IV values for all of these tiers
        if summoner["tier_division"] in UNCOMMON_TIERS:
            summoner["tier_rank_number"] = "IV"

        # calculate value by adding tier_division, tier_rank_number
        rank_value = (
            float(TIER_VALUE.get(summoner["tier_division"]))
            + RANK_VALUE.get(summoner["tier_rank_number"]) * 1000
            + summoner["league_points"]
        )

        # update so that it can be used in display teams function
        summoner.update({"rank_value": rank_value})

    # sort list of summoners by highest rank value
    sorted_list_of_summoners = sorted(
        list_of_summoners, key=lambda i: i["rank_value"], reverse=True
    )

    blue_team = list()
    red_team = list()

    # distirbute the sorted list into two different list
    for index, summoner in enumerate(sorted_list_of_summoners):
        if index % 2 == 0:
            blue_team.append(summoner)
        else:
            red_team.append(summoner)

    return blue_team, red_team
