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
    global help_title_test
    global help_description_test

    help_title_test = "How to use {} command".format(name)

    if summoner_name:
        help_description_test = "** **\n<@!{0}> **{1} summoner_name**".format(
            bot.user.id, name
        )
    else:
        help_description_test = "** **\n<@!{0}> **{1}**".format(bot.user.id, name)


def create_help_fields(name: list):
    """
    Make a global value variable for help embed message
    """
    global help_value
    help_value = ""
    for desc in name:
        help_value += desc + "\n\n"


def create_help_embed():
    """create embed for help message"""
    try:
        embed_data = EmbedData()

        embed_data.title = help_title_test

        embed_data.description = help_description_test

        embed_data.color = discord.Color.blurple()

        embed_data.fields = []

        embed_data.fields.append(
            {"name": "** **", "value": help_value, "inline": False}
        )
        embed_data.fields.append(
            {"name": "** **", "value": "`All Data from NA server`", "inline": False}
        )

        return create_embed(embed_data)

    except Exception as e_values:
        print("error embed")
        print(e_values)
