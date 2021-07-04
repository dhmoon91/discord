"""
Bot codes
"""


import os
from dotenv import load_dotenv


# saving df to image
import dataframe_image as dfi

# catching Api error
from riotwatcher import ApiError

# Discord
import discord
from discord.ext import commands

# Riot util func.
from riot import get_summoner_rank, previous_match

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
async def get_rank(ctx, *, name: str):  # using * for get a summoner name with space
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
    except ApiError as e_values:
        # 404 error means Data not found in API
        if e_values.response.status_code == 404:
            error_title = f'Summoner "{name}" is not found'
            error_description = f"Please check the summoner name agian \n \
                \n __*NOTE*__:   **{get_rank.name}** command only accepts one summoner name.\
                \n\n Please type  `rank --help`  to see how to use"
        else:
            error_title = "Error"
            error_description = "Oops! Something went wrong.\n\nPlease try again!"

        embed_data = EmbedData()
        embed_data.title = ":x:   {0}".format(error_title)
        embed_data.description = "{0}".format(error_description)
        embed_data.color = discord.Color.red()

        await ctx.send(embed=create_embed(embed_data))


@bot.command(
    name="last_match",
    help="Displays the information about the latest game of the summoner.",
)
async def get_last_match(ctx, *, name: str):
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
    except ApiError as e_values:
        if e_values.response.status_code == 404:
            error_title = f'Summoner "{name}" is not found'
            error_description = f"Please check the summoner name agian \n \
                \n __*NOTE*__ :   **{get_last_match.name}** command only accepts one summoner name.\
                \n\n Please type  `last_match --help`  to see how to use"
        else:
            error_title = "Error"
            error_description = "Oops! Something went wrong.\n\nPlease try again!"

        embed_data = EmbedData()
        embed_data.title = ":x:   {0}".format(error_title)
        embed_data.description = "{0}".format(error_description)
        embed_data.color = discord.Color.red()

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
