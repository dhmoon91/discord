"""
Help message of each commands
"""

# Discord
import discord

from utils.embed_object import EmbedData
from utils.utils import create_embed


def create_help_title_desc(bot, name, summoner_name: bool):
    """
    Make global title and description variables for help embed message
    """
    # pylint: disable=global-variable-undefined, invalid-name
    global help_title
    global help_description
    help_title = "How to use {} command".format(name)

    if summoner_name:
        help_description = "** **\n<@!{0}> **{1} summoner_name**".format(
            bot.user.id, name
        )
    else:
        help_description = "** **\n<@!{0}> **{1}**".format(bot.user.id, name)


def create_help_fields(name: list):
    """
    Make a global value variable for help embed message
    """
    # pylint: disable=global-variable-undefined, invalid-name
    global help_information
    help_information = ""
    for desc in name:
        help_information += desc + "\n\n"


def create_help_embed():
    """create embed for help message"""
    try:
        embed_data = EmbedData()

        embed_data.title = help_title

        embed_data.description = help_description

        embed_data.color = discord.Color.blurple()

        embed_data.fields = []

        embed_data.fields.append(
            {"name": "** **", "value": help_information, "inline": False}
        )

        embed_data.fields.append(
            {"name": "** **", "value": "`All Data from NA server`", "inline": False}
        )

        return create_embed(embed_data)

    # pylint: disable=broad-except
    except Exception as e_values:
        print("error embed")
        print(e_values)
        return None  # use to fix "inconsistent-return-statements" pylint error
