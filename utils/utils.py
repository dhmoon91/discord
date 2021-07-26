"""
Utils
"""

# OS
from os.path import dirname, join

# Discord
import discord

from .constants import (
    TIER_RANK_MAP,
    UNCOMMON_TIERS,
    UNCOMMON_TIER_DISPLAY_MAP,
)

root_dirname = dirname(dirname(__file__))


def get_file_path(file_path):
    """Get absolute file path"""
    return join(root_dirname, file_path)


# pylint: disable=fixme
# TODO: Properly check for each fields existence and set values.
# eg; Currently assumes title, description, color will be in 'embed_object',
# same for inner objects of 'fields', author object.
# pylint: disable=inconsistent-return-statements
def create_embed(embed_object):
    """Helper function to create embed for discords"""
    try:
        embed = discord.Embed(
            title=embed_object.title,
            description=embed_object.description,
            color=embed_object.color,
        )

        if hasattr(embed_object, "author"):
            embed.set_author(
                name=embed_object.author["name"],
                url=f"{embed_object.author['url']}",
                icon_url=embed_object.author["icon_url"],
            )

        if hasattr(embed_object, "thumbnail"):
            embed.set_thumbnail(url=f"{embed_object.thumbnail}")

        if hasattr(embed_object, "footer"):
            embed.set_footer(text=f"{embed_object.footer}")

        if hasattr(embed_object, "fields"):
            for field in embed_object.fields:
                embed.add_field(
                    name=field["name"],
                    value=field["value"],
                    inline=field["inline"],
                )

        return embed
    # pylint: disable=broad-except
    except Exception as e_values:
        print("check")
        print("error embed")
        print(e_values)


def normalize_name(string):
    """Normalize name by changing to lower case and removing whitespaces"""
    return string.lower().replace(" ", "")
<<<<<<< HEAD


def create_team_string(team_members):
    """Create red/blue team display string"""
    team_output_string = ""
    for member in team_members:
        team_output_string += (
            "`{0}{1}` {2}\n".format(
                member["tier_division"][0],
                TIER_RANK_MAP.get(member["tier_rank"]),
                member["summoner_name"],
            )
            # different formatting for uncommon tiers
            if member["tier_division"] not in UNCOMMON_TIERS
            else "`{0}` {1}\n".format(
                UNCOMMON_TIER_DISPLAY_MAP.get(member["tier_division"]),
                member["summoner_name"],
            )
        )
    return team_output_string
=======
>>>>>>> 8cfd4cb (refactoring repeated codes from bot.py)
