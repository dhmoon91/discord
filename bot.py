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


from utils.embed_object import EmbedData
from utils.utils import create_embed

intents = discord.Intents.default()
# pylint: disable=assigning-non-slot
intents.members = True  # Subscribe to the privileged members intent.

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
LOCAL_BOT_PREFIX = os.getenv("LOCAL_BOT_PREFIX")

# ADD help_command attribute to remove default help command
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(LOCAL_BOT_PREFIX),
    intents=intents,
    help_command=None,
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
        summoner_info = get_summoner_rank(name)

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


@bot.command(name="add", help="Add the players to the list")
async def add_summoner(ctx, *, message):
    """Writes list of summoners to local
    json file and sends the list to the bot"""

    try:
        # typing indicator
        async with ctx.typing():
            await asyncio.sleep(1)

        json_path = "data/data.json"

        # create a directory containing json file to store data for added summoners
        if not os.path.exists(json_path):
            os.makedirs("data")
            with open(json_path, "w"):
                pass

        # accepting comma, space and comma plus space
        # TODO: !add lifeissohard 들어올때 input을 애초에 space가 아예 없이 받고, 그리고 data.json에 저장할때도 이름을 space 없이 저장하기
        player_list = message.replace(" ","").lower().split(",")

        # for importing data from json file
        file_data = ""

        # initializing total number of players for counting both incoming and existing summoners
        total_number_of_players = 0

        # initializing server id to a variable
        server_id = str(ctx.guild.id)

        # storing the json file into a variable
        if os.path.getsize(json_path) > 0:
            with open(json_path, "r") as file:
                # TODO: check if you can load part of the json file (specific server id data)
                file_data = json.load(file)

            # if server id exist in json, add number of players
            if server_id in file_data:
                total_number_of_players += len(file_data[server_id])
                
            # remove summoners from incoming data if it exists in json file with same server ID
            for count, player_name in enumerate(player_list):
                if any(player_name in player["user_name"] for player in file_data[server_id]):
                    player_list.remove(player_name)

            # add number of summoners from incoming data to total number of players
            total_number_of_players += len(player_list)    

        if total_number_of_players > 10:
            # TODO: throw error
            print("THROW with a message")
        # send error message to bot then exits out of the function if an error with summoner's name
        for player_name in enumerate(player_list):
            if not check_summoner_name(player_name):
                embed = discord.Embed(
                    title=":x:   Invalid Summoner Name",
                    description=f"`{player_name}` is not a valid summoner name.",
                    color=discord.Color.red(),
                )

                embed.add_field(
                    name="** **",
                    value="Please enter a valid summoner name!",
                    inline=False,
                )

                embed.add_field(
                    name="** **",
                    value=f"Adding multiple summoners:\n`@{bot.user.name} add name1, name2`",
                    inline=False,
                )

                await ctx.send(embed=embed)
                return None

            # changes the incoming summoner names to what's in the api
            # NOT needed since there won't be any space in summoner name in json data
            players_list[count] = get_summoner_name(players_list[count])

            # if summoner name in the json file, remove summoner from adding to the list
            if os.path.getsize(json_path) > 0 and any(
                players_list[count] in player["user_name"]
                for player in file_data[server_id]
            ):
                players_list.remove(players_list[count])

        # add number of players from incoming data
        number_of_players += len(players_list)

        # if more than 10 players, send error message
        # TODO: throw message
        if number_of_players > 10:
            num_of_players_needed = 10 - len(file_data[server_id])
            await ctx.send("You have exceeded limit of 10 summoners!\n")
            await ctx.send(f"Please add {num_of_players_needed} more summoners!\n")

        # TODO: in data.json store as
        #name: lifeissohard
        #name_in_api: Life is so hard

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

    # 이거 따로 function으로 빼기

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
    except Exception as e:
        # TODO: 404 (data not found) OR general output like Oops something went wrong! Try again!


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
