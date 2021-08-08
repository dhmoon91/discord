"""
Bot codes
"""


import os
import asyncio
import pydash

from dotenv import load_dotenv

# DB
from sqlalchemy import create_engine

# Discord
import discord
from discord.ext import commands

from db.db import bind_engine, Session
from db.models.team_members import TeamMembers
from db.models.channels import Channels
from db.utils import check_cached

# Riot util func.
from riot_api import (
    get_summoner_rank,
    create_summoner_list,
)

from utils.embed_object import EmbedData
from utils.utils import (
    create_embed,
    get_file_path,
    normalize_name,
    create_team_string,
    get_region,
)
from utils.make_teams import make_teams
from utils.constants import (
    TIER_RANK_MAP,
    MAX_NUM_PLAYERS_TEAM,
    UNCOMMON_TIERS,
    UNCOMMON_TIER_DISPLAY_MAP,
    REGION_MAP,
    REGION_DISPLAY_MAP,
)

intents = discord.Intents.default()
# pylint: disable=assigning-non-slot
intents.members = True  # Subscribe to the privileged members intent.


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
LOCAL_BOT_PREFIX = os.getenv("LOCAL_BOT_PREFIX")
DB_URL = os.getenv("DB_URL")

# differ by env.
# Connec to DB.
engine = create_engine(DB_URL)
bind_engine(engine)
session = Session()

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


@bot.command(name="region", help="Set region for data pull")
async def set_region(ctx, *, message):
    """
    Set region for data pull
    """

    try:
        async with ctx.typing():
            await asyncio.sleep(1)

        # Clean out the input
        if REGION_MAP.get(message.lower().strip()) is None:
            print("Invalid region input")
            raise Exception(
                "Invalid region input", "Available regions: NA, KR, EUW, EUN, JP"
            )

        region = REGION_MAP[message.lower().strip()]

        # initializing server id.
        server_id = str(ctx.guild.id)

        # Grab team member list from db
        channel_saved = check_cached(server_id, Channels, Channels.channel_id)
        if channel_saved is None:
            region_data = Channels(
                str(ctx.guild.id),
                region,
            )
            region_data.create()
        else:
            print("UPDATE RECORD")
            channel_saved_result = (
                session.query(Channels)
                .filter(Channels.channel_id == server_id)
                .one_or_none()
            )
            channel_saved_result.region = region

            # Update record.
            # TODO: Simplify this - use base.py - update()
            try:
                session.commit()
            except Exception as e_value:
                session.rollback()
                raise e_value
            finally:
                session.close()
        # Return success message
        embed_data = EmbedData()
        embed_data.title = "Region successfully updated"
        embed_data.description = f"All data will be pulled from {region}"
        embed_data.color = discord.Color.green()

        await ctx.send(embed=create_embed(embed_data))
    except Exception as e_values:
        error_title = "Error"
        error_description = (
            "Oops! Something went wrong.\
                \n\n Please type  `rank --help`  to see how to use and try again!",
        )
        color = discord.Color.red()

        if "Invalid region input" in str(e_values):
            error_title = e_values.args[0]
            error_description = e_values.args[1]

        embed_data = EmbedData()
        embed_data.title = ":x:   {0}".format(error_title)
        embed_data.description = "{0}".format(error_description)
        embed_data.color = color
        await ctx.send(embed=create_embed(embed_data))


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
            f"`All Data from {REGION_DISPLAY_MAP.get(get_region( str(ctx.guild.id)))} "
            f"server`\n\n <@!{bot.user.id}> <command>"
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

    except Exception:
        err_embed = discord.Embed(
            title="Error",
            description="Oops! Something went wrong.\
              \n\n Please type  `rank --help`  to see how to use and try again!",
            color=discord.Color.red(),
        )

        await ctx.send(embed=err_embed)


@bot.command(name="rank", help="Displays the information about the summoner.")
async def get_rank(ctx, *, name: str):  # using * for get a summoner name with space
    """Sends the summoner's rank information to the bot"""
    try:
        # typing indicator
        async with ctx.typing():
            await asyncio.sleep(1)

        summoner_info = get_summoner_rank(name, get_region(str(ctx.guild.id)))

        embed_data = EmbedData()
        embed_data.title = "Solo/Duo Rank"

        embed_data.color = discord.Color.dark_gray()

        # Add author, thumbnail, fields, and footer to the embed
        embed_data.author = {}
        embed_data.author = {
            "name": summoner_info["summoner_name"],
            # For op.gg link, we have to remove all whitespace.
            "url": "https://na.op.gg/summoner/userName={0}".format(
                summoner_info["summoner_name"].replace(" ", "")
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

        # Due to zero division error, need to handle situation where total games are zero
        solo_rank_win_percentage = (
            0
            if summoner_total_game == 0
            else int(summoner_info["solo_win"] / summoner_total_game * 100)
        )

        embed_data.description = "**{0[tier]}**   {0[league_points]}LP \
                    \nTotal Games Played: {1}\n{0[solo_win]}W {0[solo_loss]}L {2}%".format(
            summoner_info,
            summoner_total_game,
            solo_rank_win_percentage,
        )

        embed_data.fields = []
        embed_data.fields.append(
            {
                "name": "** **",
                "value": (
                    f"`All Data from {REGION_DISPLAY_MAP.get(get_region(str(ctx.guild.id)))}"
                    " server`"
                ),
                "inline": False,
            }
        )

        await ctx.send(file=file, embed=create_embed(embed_data))

    except Exception as e_values:
        print(e_values)
        # 404 error means Data not found in API
        if "404" in str(e_values):
            error_title = f'Summoner "{name}" is not found'
            error_description = f"Please check the summoner name agian \n \
              \n __*NOTE*__:   **{get_rank.name}** command only accepts one summoner name.\
              \n\n Please type  `rank --help`  to see how to use"
        else:
            error_title = "Error"
            error_description = "Oops! Something went wrong.\
              \n\nPlease type  `rank --help`  to see how to use and tyr again!"

        embed_data = EmbedData()
        embed_data.title = ":x:   {0}".format(error_title)
        embed_data.description = "{0}".format(error_description)
        embed_data.color = discord.Color.red()

        await ctx.send(embed=create_embed(embed_data))


@bot.command(name="add", help="Add the players to the list")
async def add_summoner(ctx, *, message):
    """Writes list of summoners to local
    json file and sends the list to the bot"""

    try:
        # typing indicator
        async with ctx.typing():
            await asyncio.sleep(1)

        # converting the message into list of summoners
        # Split by ',' and remove leading/trailling white spaces.
        user_input_names = [x.strip() for x in message.split(",")]

        # initializing server id to a variable
        server_id = str(ctx.guild.id)

        # initializing total number of players for counting both incoming and existing summoners
        total_number_of_players = 0

        # Grab team member list from db
        members_list_record_cached = check_cached(
            server_id, TeamMembers, TeamMembers.channel_id
        )

        # If we have record;
        # Check # of players that were save in the list.
        # Remove names from user input if we already have the name in record.
        if members_list_record_cached:
            # Convert into dict.
            total_number_of_players += len(
                members_list_record_cached["dict"]["members"]
            )

            for member in members_list_record_cached["dict"]["members"]:
                record_name = member["summoner_name"]
                name_record_input_match = pydash.find(
                    user_input_names,
                    lambda input_name: (input_name == record_name),
                )

                if name_record_input_match:
                    user_input_names.remove(name_record_input_match)

        # 'user_input_names' should be filtered with names that we don't have record of.
        total_number_of_players += len(user_input_names)

        # If 'total_number_of_players' will be more than 10, error out.
        if total_number_of_players > MAX_NUM_PLAYERS_TEAM:
            raise Exception(
                "Limit Exceeded",
                "You have exceeded a limit of 10 summoners! \
                \nPlease add {0} more summoners!".format(
                    MAX_NUM_PLAYERS_TEAM
                    - total_number_of_players
                    + len(user_input_names)
                ),
            )

        # If all the summoners are already in record, return.
        if total_number_of_players == 0:
            await display_current_list_of_summoners(ctx)
            return

        # make dictionary for newly coming in players
        new_team_members = create_summoner_list(
            user_input_names, get_region(str(ctx.guild.id))
        )

        # If we had a db record, update.
        if members_list_record_cached:
            # Get original list
            members_update = members_list_record_cached["dict"]["members"]

            # Append new players
            for player_list in new_team_members:
                members_update.append(player_list)

            # Set new member list.
            # Note; was going to use members_list_record_cached['raw'] to update,
            # but looks like it doesn't work.
            member_list_query_result = (
                session.query(TeamMembers)
                .filter(TeamMembers.channel_id == server_id)
                .one_or_none()
            )
            member_list_query_result.members = members_update

            # Update record.
            # TODO: Simplify this - use base.py - update()
            try:
                session.commit()
            except Exception as e_value:
                session.rollback()
                raise e_value
            finally:
                session.close()
        else:
            # If we don't have a record, create one.
            members_create_data = []
            # TODO: No need to group by server_id once we have everything migrated to db.
            for new_player in new_team_members:
                members_create_data.append(new_player)
            create_member = TeamMembers(server_id, members_create_data)
            create_member.create()

        # display list of summoners
        await display_current_list_of_summoners(ctx)

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
        # TODO this shouldn't call another decorator function.
        await display_current_list_of_summoners(ctx)


# TODO Refactor into util function.
@bot.command(name="list", help="Display list of summoner")
async def display_current_list_of_summoners(ctx):
    """For displaying current list of summoners"""
    try:
        # server id
        server_id = str(ctx.guild.id)

        total_number_of_players = 0

        # Grab team member list from db
        members_list_record_cached = check_cached(
            server_id, TeamMembers, TeamMembers.channel_id
        )

        # If no record, error out.
        if members_list_record_cached is None:
            raise Exception("NO SUMMONERS IN THE LIST")

        # If we have record, print
        total_number_of_players += len(members_list_record_cached["dict"]["members"])

        # making embed for list of summoners
        embed_data = EmbedData()
        embed_data.title = "List of Summoners"
        embed_data.description = "** **"
        embed_data.color = discord.Color.dark_gray()

        # for saving output str
        output_str = ""
        for member in members_list_record_cached["dict"]["members"]:
            output_str += (
                "`{0}` {1}\n".format(
                    UNCOMMON_TIER_DISPLAY_MAP.get(member["tier_division"]),
                    member["summoner_name"],
                )
                if member["tier_division"] in UNCOMMON_TIERS
                else "`{0}{1}` {2}\n".format(
                    member["tier_division"][0],
                    TIER_RANK_MAP.get(member["tier_rank"]),
                    member["summoner_name"],
                )
            )

        embed_data.fields = []
        embed_data.fields.append(
            {"name": "Summoners", "value": output_str, "inline": False}
        )

        await ctx.send(embed=create_embed(embed_data))

        await ctx.send(f"Total Number of Summoners: {total_number_of_players}")

    except Exception:
        embed_data = EmbedData()
        embed_data.title = ":warning:   No Summoners in the List"
        embed_data.description = f"Please add summoner by `@{bot.user.name} add`"
        embed_data.color = discord.Color.orange()
        await ctx.send(embed=create_embed(embed_data))


@bot.command(name="teams", help="Display two teams")
async def display_teams(ctx):
    """Make and display teams to bot from list of summoners in json"""
    try:
        # typing indicator
        async with ctx.typing():
            await asyncio.sleep(1)

        # server id
        server_id = str(ctx.guild.id)

        # Grab team member list from db
        members_list_record_cached = check_cached(
            server_id, TeamMembers, TeamMembers.channel_id
        )

        # If no record, error out.
        if members_list_record_cached is None:
            raise Exception("NO SUMMONERS IN THE LIST")

        # Error out if we don't have 10 players
        if len(members_list_record_cached["dict"]["members"]) != 10:
            raise Exception("NOT ENOUGH PLAYERS")

        teams = make_teams(members_list_record_cached["dict"]["members"])

        blue_team = teams[0]
        red_team = teams[1]

        blue_team_output = create_team_string(blue_team)
        red_team_output = create_team_string(red_team)

        for team_name in ["blue", "red"]:
            embed_data = EmbedData()
            embed_data.title = f"TEAM {team_name.upper()}"
            embed_data.description = "** **"
            embed_data.color = (
                discord.Color.blue() if team_name == "blue" else discord.Color.red()
            )
            file = discord.File(get_file_path(f"images/{team_name}-minion.png"))
            embed_data.thumbnail = f"attachment://{team_name}-minion.png"
            embed_data.fields = []
            embed_data.fields.append(
                {
                    "name": "Summoners" + " " * 10,
                    "value": blue_team_output
                    if team_name == "blue"
                    else red_team_output,
                    "inline": True,
                }
            )
            await ctx.send(file=file, embed=create_embed(embed_data))

    except Exception as e_values:
        if str(e_values) in ["NOT ENOUGH PLAYERS", "NO SUMMONERS IN THE LIST"]:
            error_title = e_values.args[0]
            error_description = f"There are not enough players to make teams \
                \n\nTo add a summoner:\n`@{bot.user.name} add summoner_name` \
                    \n\nAdding multiple summoners:\n `@{bot.user.name} add name1, name2`"
        else:
            error_title = f"{e_values}"
            error_description = "Oops! Something went wrong.\nTry again!"

        embed_data = EmbedData()
        embed_data.title = ":x:   {0}".format(error_title)
        embed_data.description = "{0}".format(error_description)
        embed_data.color = discord.Color.red()
        await ctx.send(embed=create_embed(embed_data))


@bot.command(name="remove", help="Remove player(s) from the list")
async def remove_summoner(ctx, *, message):
    """Remove summoner(s) from list
    and send  the list to the bot"""

    try:
        # typing indicator
        async with ctx.typing():
            await asyncio.sleep(1)

        # converting the message into list of summoners
        summoner_to_remove_input = [x.strip() for x in message.split(",")]

        # Exception case: attempt to remove more than 10 players
        if len(summoner_to_remove_input) > MAX_NUM_PLAYERS_TEAM:
            raise Exception(
                "Limit Exceeded",
                "You tried to remove more than 10 summoners! \
                \nPlease remove {0} less summoners or consider using `clear` command".format(
                    MAX_NUM_PLAYERS_TEAM - len(summoner_to_remove_input)
                ),
            )
        # initializing server id to a variable
        server_id = str(ctx.guild.id)

        # Grab team member list from db
        members_list_record_cached = check_cached(
            server_id, TeamMembers, TeamMembers.channel_id
        )

        # Exception case: data/data.json file does not exist
        if members_list_record_cached is None:
            raise Exception(
                "No summoners added",
                "There is no summoner(s) added in the game.\nPlease add summoner(s) first!",
            )

        # initializing server id to a variable
        server_id = str(ctx.guild.id)

        unmatched_summoner_name = []
        for remove_name in summoner_to_remove_input:
            # members_list_record_cached["dict"]["members"]:
            matched_summoner = pydash.find(
                members_list_record_cached["dict"]["members"],
                lambda x: normalize_name(x["summoner_name"])
                == normalize_name(remove_name),
            )

            if matched_summoner is None:
                unmatched_summoner_name.append(remove_name)
                continue

            members_list_record_cached["dict"]["members"].remove(matched_summoner)

        if len(unmatched_summoner_name) > 0:
            raise Exception(
                "Unregistered Summoner(s)",
                "Summoners: {0} were not registered for the game".format(
                    str(unmatched_summoner_name)
                ),
            )

        member_list_query_result = (
            session.query(TeamMembers)
            .filter(TeamMembers.channel_id == server_id)
            .one_or_none()
        )

        member_list_query_result.members = members_list_record_cached["dict"]["members"]

        # Update record.
        # TODO: Simplify this - use base.py - update()
        try:
            session.commit()
        except Exception as e_value:
            session.rollback()
            raise e_value
        finally:
            session.close()

        # display list of summoners
        await display_current_list_of_summoners(ctx)

    except Exception as e_values:
        if "Limit Exceeded" in str(e_values) or "Unregistered Summoner(s)" in str(
            e_values
        ):
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


@bot.command(name="clear", help="Clear player(s) from the list")
async def clear_list_of_summoners(ctx):
    """Clear out summoners from the list"""

    try:
        server_id = str(ctx.guild.id)
        member_list_query_result = (
            session.query(TeamMembers).filter(TeamMembers.channel_id == server_id).one()
        )
        member_list_query_result.delete(session)

        # display list of summoners
        await display_current_list_of_summoners(ctx)

    except Exception as e_values:
        error_title = f"{e_values}"
        error_description = "Oops! Something went wrong.\nTry again!"

        embed_data = EmbedData()
        embed_data.title = ":x:   {0}".format(error_title)
        embed_data.description = "{0}".format(error_description)
        embed_data.color = discord.Color.red()
        await ctx.send(embed=create_embed(embed_data))

        # display list of summoners
        await display_current_list_of_summoners(ctx)


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
