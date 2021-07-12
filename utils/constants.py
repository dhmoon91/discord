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
    "MASTER": 7,
    "GRANDMASTER": 8,
    "CHALLENGER": 9,
}

RANK_VALUE = {"I": 0.75, "II": 0.5, "III": 0.25, "IV": 0}
