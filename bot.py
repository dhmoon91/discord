"""
Bot codes
"""


import os
import json
import asyncio

from dotenv import load_dotenv

# saving df to image
import dataframe_image as dfi

# Discord
import discord
from discord.ext import commands

# Riot util func.
from riot import (
    get_summoner_rank,
    previous_match,
    create_summoner_list,
    check_summoner_name,
    get_summoner_name,
)


intents = discord.Intents.default()
# pylint: disable=assigning-non-slot
intents.members = True  # Subscribe to the privileged members intent.

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
LOCAL_BOT_PREFIX = os.getenv("LOCAL_BOT_PREFIX")

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(LOCAL_BOT_PREFIX), intents=intents
)


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


@bot.command(name="rank", help="Get rank of summoner")
async def get_rank(ctx, name: str):
    """Sends the summoner's rank information to the bot"""
    summoner_info = get_summoner_rank(name)

    embed = discord.Embed(title="Solo/Duo Rank", color=discord.Color.dark_gray())

    summoner_name = summoner_info["user_name"]

    # Removing space of the summoner name to access op.gg url of the summoner
    summoner_name_opgg = summoner_name.replace(" ", "")

    # Add author, thumbnail, fields, and footer to the embed
    embed.set_author(
        name=summoner_name,
        url=f"https://na.op.gg/summoner/userName={summoner_name_opgg}",
        icon_url=summoner_info["summoner_icon_image_url"],
    )

    # Get image of tier by path
    tier_image = summoner_info["tier_image"]
    file = discord.File(tier_image)
    # Need to get the filename in order to attach to the thumbnail
    tier_image_filename = tier_image.replace("ranked-emblems/", "")
    # Embed thumbnail image of tier at the side of the embed
    embed.set_thumbnail(url=f"attachment://{tier_image_filename}")

    # Setting variables for summoner information to display as field
    summoner_rank = summoner_info["tier"]
    solo_win = summoner_info["solo_win"]
    solo_loss = summoner_info["solo_loss"]
    summoner_total_game = solo_win + solo_loss
    solo_rank_percentage = int(solo_win / summoner_total_game * 100)

    embed.add_field(
        name=summoner_rank,
        value="Total Games Played:"
        + f"{summoner_total_game}\n{solo_win}W \
          {solo_loss}L {solo_rank_percentage}%",
        inline=False,
    )
    await ctx.send(file=file, embed=embed)


@bot.command(name="last_match", help="Get last match history")
async def get_last_match(ctx, name: str):
    """Sends the summoner's last match information to the bot"""
    last_match_info = previous_match(name)
    dfi.export(last_match_info, "df_styled.png")
    file = discord.File("df_styled.png")
    embed = discord.Embed()
    embed.set_image(url="attachment://df_styled.png")
    await ctx.send(embed=embed, file=file)
    os.remove("df_styled.png")


@bot.command(name="add", help="Add the players to the list")
async def add_summoner(ctx, *, message):
    """Writes list of summoners to local
    json file and sends the list to the bot"""

    async with ctx.typing():
        await asyncio.sleep(1)

    json_path = "data/data.json"

    # create a directory containing json file to store data for added summoners
    if not os.path.exists(json_path):
        os.makedirs("data")
        with open(json_path, "w"):
            pass

    # accepting comma, space and comma plus space
    players_list = [x.strip() for x in message.replace(" ", ",").split(",")]
    players_list = list(filter(None, players_list))

    file_data = ""

    # initializing number of players to display
    number_of_players = 0

    # initializing server id to a variable
    server_id = str(ctx.guild.id)

    # storing the json file into a variable
    if os.path.getsize(json_path) > 0:
        with open(json_path, "r") as file:
            file_data = json.load(file)

        # if server id exist in json, add number of players
        if server_id in file_data:
            number_of_players += len(file_data[server_id])

        # send error message to bot then exits out of the function if an error with summoner's name
        for count, _ in enumerate(players_list):
            if not check_summoner_name(players_list[count]):
                embed = discord.Embed(
                    title=":x:   Invalid Summoner Name",
                    description=f"`{players_list[count]}` is not a valid summoner name.\n\n \
                    Please enter a valid summoner name!",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
                return None

            # changes the incoming summoner names to what's in the api
            players_list[count] = get_summoner_name(players_list[count])

            # if summoner name in the json file, remove summoner from adding to the list
            if any(
                players_list[count] in player["user_name"]
                for player in file_data[server_id]
            ):
                players_list.remove(players_list[count])

    # add number of players from incoming data
    number_of_players += len(players_list)

    # if more than 10 players, send error message
    if number_of_players > 10:
        num_of_players_needed = 10 - len(file_data[server_id])
        await ctx.send("You have exceeded limit of 10 summoners!\n")
        await ctx.send(f"Please add {num_of_players_needed} more summoners!\n")

    else:
        # make dictionary for newly coming in players
        players_list_info = create_summoner_list(players_list, server_id)

        # if there is less than or equal to total of 10 players

        await ctx.send(f"Total Number of Summoners: {number_of_players}")

        # if no file exist in path or if the file is empty, dump incoming data
        if not os.path.isfile(json_path) or os.path.getsize(json_path) == 0:
            with open(json_path, "w") as file:
                json.dump(players_list_info, file, indent=4)
                file_data = players_list_info

        # append data to the matching server id
        else:
            file_data[server_id] += players_list_info[server_id]

            with open(json_path, "w") as file:
                json.dump(file_data, file, indent=4)

    embed = discord.Embed(title="List of Summoners", color=discord.Color.dark_gray())

    output_str = ""

    for count in range(len(file_data[server_id])):

        output_str += (
            "`"
            + file_data[server_id][count]["tier_division"][0]
            + file_data[server_id][count]["tier_rank_number"]
            + "` "
            + file_data[server_id][count]["user_name"]
            + "\n"
        )

    embed.add_field(
        name="Summoners",
        value=output_str,
        inline=False,
    )

    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    """Checks error and sends error message if exists"""
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")


bot.run(TOKEN)
