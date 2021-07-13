"""
Bot codes
"""


import os
import json
import asyncio

from dotenv import load_dotenv

# DB
from sqlalchemy import create_engine
from db.db import bind_engine, Session
from db.models.summoners import Summoners

# saving df to image
import dataframe_image as dfi

# Discord
import discord
from discord.ext import commands

# Riot util func.
from riot import get_summoner_rank, previous_match, create_summoner_list


from utils.embed_object import EmbedData
from utils.utils import create_embed, get_file_path
from utils.constants import TIER_RANK_MAP, MAX_NUM_PLAYERS_TEAM

intents = discord.Intents.default()
# pylint: disable=assigning-non-slot
intents.members = True  # Subscribe to the privileged members intent.

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
LOCAL_BOT_PREFIX = os.getenv("LOCAL_BOT_PREFIX")

# TODO: differ by env.
# Init DB
engine = create_engine("postgresql://admin_bot:test@localhost/bot_dev")
bind_engine(engine)
session = Session()

# ADD help_command attribute to remove default help command
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(LOCAL_BOT_PREFIX),
    intents=intents,
    help_command=None,
)

# folder and path for data json
data_folder_path = get_file_path("data/")
json_path = data_folder_path + "data.json"


@bot.event
async def on_ready():
    """Prints that the bot is connected"""
    print(f"{bot.user.name} has connected to Discord!")


@bot.event
async def on_member_join(member):
    """Sends personal discord message to the membed who join"""
    # create a direct message channel.
    await member.create_dm()
    # Send welcome msg.
    await member.dm_channel.send(f"Hi {member.name}, welcome to 관전남 월드!")


# Custom help command
@bot.command(
    name="help",
    help="Displays the syntax and the description of all the commands.",
)
async def help_command(ctx):
    """Help command outputs description about all the commands"""
    try:
        embed_data = EmbedData()
        embed_data.title = f"How to use {bot.user.name}"
        embed_data.description = (
            f"`All Data from NA server`\n\n <@!{bot.user.id}> <command>"
        )
        embed_data.color = discord.Color.gold()

        # ADD thumbnail (Image can be changed whatever we want. eg.our logo)
        embed_data.thumbnail = "https://emoji.gg/assets/emoji/3907_lol.png"

        embed_data.fields = []
        embed_data.fields.append({"name": "** **", "value": "** **", "inline": False})

        for command in bot.commands:
            if not str(command).startswith("help"):
                embed_data.fields.append(
                    {
                        "name": "** **",
                        "value": f"<@!{bot.user.id}> **{command.name} summoner_name** \n \
                            {command.help}",
                        "inline": False,
                    }
                )
        await ctx.send(embed=create_embed(embed_data))
        # pylint: disable=broad-except
    except Exception as e_values:
        print(e_values)


@bot.command(name="rank", help="Displays the information about the summoner.")
async def get_rank(ctx, name: str):
    """Sends the summoner's rank information to the bot"""
    try:
        channel_id = str(ctx.guild.id)
        summoner_info = get_summoner_rank(name)
        summoner_data = Summoners(
            channel_id,
            "NA",
            summoner_info["puuid"],
            summoner_info["tier_division"],
            summoner_info["tier_rank"],
            summoner_info["solo_win"],
            summoner_info["solo_loss"],
        )
        # Create db row.
        session.add(summoner_data)
        session.commit()

        embed_data = EmbedData()
        embed_data.title = "Solo/Duo Rank"
        embed_data.description = (
            f"`All Data from NA server`\n\n <@!{bot.user.id}> <command>"
        )
        embed_data.color = discord.Color.dark_gray()

        # Add author, thumbnail, fields, and footer to the embed
        embed_data.author = {}
        embed_data.author = {
            "name": summoner_info["user_name"],
            # For op.gg link, we have to remove all whitespace.
            "url": "https://na.op.gg/summoner/userName={0}".format(
                summoner_info["user_name"].replace(" ", "")
            ),
            "icon_url": summoner_info["summoner_icon_image_url"],
        }

        # Upload tier image to discord to use it as thumbnail of embed using full path of image.
        file = discord.File(summoner_info["tier_image_path"])

        # Embed thumbnail image of tier at the side of the embed
        # Note: This takes the 'file name', not a full path.
        embed_data.thumbnail = "attachment://{0[tier_image_name]}".format(summoner_info)

        # Setting variables for summoner information to display as field
        summoner_total_game = summoner_info["solo_win"] + summoner_info["solo_loss"]
        solo_rank_win_percentage = int(
            summoner_info["solo_win"] / summoner_total_game * 100
        )

        embed_data.fields = []
        embed_data.fields.append(
            {
                "name": "{0[tier]}".format(summoner_info),
                "value": "Total Games Played: {1}\n{0[solo_win]}W {0[solo_loss]}L {2}%".format(
                    summoner_info,
                    summoner_total_game,
                    solo_rank_win_percentage,
                ),
                "inline": False,
            }
        )
        await ctx.send(file=file, embed=create_embed(embed_data))
        # pylint: disable=broad-except
    except Exception as e_values:
        print(e_values)


@bot.command(
    name="last_match",
    help="Displays the information about the latest game of the summoner.",
)
async def get_last_match(ctx, name: str):
    """Sends the summoner's last match information to the bot"""
    try:
        last_match_info = previous_match(name)
        dfi.export(last_match_info, "df_styled.png")
        file = discord.File("df_styled.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://df_styled.png")
        await ctx.send(embed=embed, file=file)
        os.remove("df_styled.png")
        # pylint: disable=broad-except
    except Exception as e_values:
        print(e_values)


# pylint: disable=too-many-locals, too-many-branches, too-many-statements
@bot.command(name="add", help="Add the players to the list")
async def add_summoner(ctx, *, message):
    """Writes list of summoners to local
    json file and sends the list to the bot"""

    try:
        # typing indicator
        async with ctx.typing():
            await asyncio.sleep(1)

        # create a directory containing json file to store data for added summoners
        if not os.path.exists(json_path):
            os.makedirs(data_folder_path, exist_ok=True)
            with open(json_path, "w"):
                pass

        # converting the message into list of summoners
        player_list = message.split(",")

        # for importing data from json file
        file_data = ""

        # initializing total number of players for counting both incoming and existing summoners
        total_number_of_players = 0

        # initializing server id to a variable
        server_id = str(ctx.guild.id)

        # storing the json file into a variable
        if os.path.getsize(json_path) > 0:
            with open(json_path, "r") as file:
                file_data = json.load(file)

            # if server id exist in json, add number of players
            if server_id in file_data:
                total_number_of_players += len(file_data[server_id])

                # remove summoners from incoming data if it exists in json file with same server ID
                for player_name in player_list:
                    if any(
                        player_name in player["user_name"]
                        for player in file_data[server_id]
                    ):
                        player_list.remove(player_name)

        # add number of summoners from incoming data to total number of players
        total_number_of_players += len(player_list)

        if total_number_of_players > MAX_NUM_PLAYERS_TEAM:
            raise Exception(
                "Limit Exceeded",
                "You have exceeded a limit of 10 summoners! \
                \nPlease add {0} more summoners!".format(
                    MAX_NUM_PLAYERS_TEAM - total_number_of_players + len(player_list)
                ),
            )

        # make dictionary for newly coming in players
        players_list_info = create_summoner_list(player_list, server_id)

        # if no file exist in path or if the file is empty, dump incoming data
        if os.path.getsize(json_path) == 0:
            with open(json_path, "w") as file:
                json.dump(players_list_info, file, indent=4)
                file_data = players_list_info

        elif server_id not in file_data:

            file_data.update(players_list_info)

            with open(json_path, "w") as file:
                json.dump(file_data, file, indent=4)

        # append data to the matching server id
        else:
            file_data[server_id] += players_list_info[server_id]

            with open(json_path, "w") as file:
                json.dump(file_data, file, indent=4)

        # display list of summoners
        await display_current_list_of_summoners(ctx)

    # pylint: disable=broad-except
    except Exception as e_values:

        if "404" in str(e_values):
            error_title = "Invalid Summoner Name"
            error_description = f"`{e_values.args[1]}` is not a valid name. \
                \n\nAdding multiple summoners:\n `@{bot.user.name} add name1, name2`"
        elif "Limit Exceeded" in str(e_values):
            error_title = e_values.args[0]
            error_description = e_values.args[1]
        else:
            error_title = f"{e_values}"
            error_description = "Oops! Something went wrong.\nTry again!"

        embed_data = EmbedData()
        embed_data.title = ":x:   {0}".format(error_title)
        embed_data.description = "{0}".format(error_description)
        embed_data.color = discord.Color.red()
        await ctx.send(embed=create_embed(embed_data))

        # display list of summoners
        await display_current_list_of_summoners(ctx)


@bot.command(name="list", help="Display list of summoner")
async def display_current_list_of_summoners(ctx):
    """For displaying current list of summoners"""

    try:
        # server id
        server_id = str(ctx.guild.id)

        file_data = ""

        if os.path.getsize(json_path) == 0 or not os.path.exists(json_path):
            raise Exception

        # get data from the json file and save to file data

        with open(json_path, "r") as file:
            file_data = json.load(file)

        if not file_data[server_id]:
            raise Exception

        total_number_of_players = len(file_data[server_id])

        # making embed for list of summoners
        embed_data = EmbedData()
        embed_data.title = "List of Summoners"
        embed_data.description = "** **"
        embed_data.color = discord.Color.dark_gray()

        # for saving output str
        output_str = ""

        for count in range(len(file_data[server_id])):

            output_str += "`{0}{1}` {2}\n".format(
                file_data[server_id][count]["tier_division"][0],
                TIER_RANK_MAP.get(file_data[server_id][count]["tier_rank_number"]),
                file_data[server_id][count]["formatted_user_name"],
            )

        embed_data.fields = []
        embed_data.fields.append(
            {"name": "Summoners", "value": output_str, "inline": False}
        )

        await ctx.send(embed=create_embed(embed_data))

        await ctx.send(f"Total Number of Summoners: {total_number_of_players}")

    # pylint: disable=broad-except
    except Exception:
        embed_data = EmbedData()
        embed_data.title = ":warning:   No Summoners in the List"
        embed_data.description = f"Please add summoner by `@{bot.user.name} add`"
        embed_data.color = discord.Color.orange()
        await ctx.send(embed=create_embed(embed_data))


@bot.event
async def on_command_error(ctx, error):
    """Checks error and sends error message if exists"""
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")

    # Send an error message when the user input invalid command
    elif isinstance(error, commands.CommandNotFound):
        err_embed = discord.Embed(
            title=f":warning:   {error}",
            description="Please type  `help`  to see how to use",
            color=discord.Color.orange(),
        )

        await ctx.send(embed=err_embed)


bot.run(TOKEN)
