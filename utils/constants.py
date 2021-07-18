"""
Constants that are used globally
"""

# roman number to numerical except for unranked
TIER_RANK_MAP = {"I": "1", "II": "2", "III": "3", "IV": "4", "R": "R"}

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
