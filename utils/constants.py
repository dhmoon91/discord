"""
Constants that are used globally
"""

# roman number to numerical except for unranked
TIER_RANK_MAP = {"I": "1", "II": "2", "III": "3", "IV": "4"}

# maximum number of players that can be added
MAX_NUM_PLAYERS_TEAM = 10

# tiers with default I rank numbers, which include master, grandmaster, challenger
UNCOMMON_TIERS = ["UNRANKED", "MASTER", "GRANDMASTER", "CHALLENGER"]

# for displaying uranked, master, grandmaster, challenger
UNCOMMON_TIER_DISPLAY_MAP = {
    "UNRANKED": "UR",
    "MASTER": "MA",
    "GRANDMASTER": "GM",
    "CHALLENGER": "CH",
}
TIER_VALUE = {
    "UNRANKED": 3,
    "IRON": 1,
    "BRONZE": 2,
    "SILVER": 3,
    "GOLD": 4,
    "PLATINUM": 5,
    "DIAMOND": 6,
    # master, grandmaster, challenger only have lp points starting 0lp for master,
    # around 300lp for grandmaster and 650lp for master
    # these are not fixed lp points as they are assigned to GM or Challenger
    # depending on the ranking not based on how much lp points they have
    # Challenger: 1 ~ 300, GrandMaster: 301 ~ 1000
    "MASTER": 7,
    "GRANDMASTER": 7,
    "CHALLENGER": 7,
}

RANK_VALUE = {"I": 0.75, "II": 0.5, "III": 0.25, "IV": 0}
