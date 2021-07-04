"""
Bot codes
"""


import os
from dotenv import load_dotenv


# saving df to image
import dataframe_image as dfi

# Discord
import discord
from discord.ext import commands

# Riot util func.
from riot import get_summoner_rank, previous_match

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

    help_embed = discord.Embed(
        title=f"How to use {bot.user.name}",
        description=f"`All Data from NA server`\n\n <@!{bot.user.id}> <command>",
        color=discord.Color.gold(),
    )

    # ADD thumbnail (Image can be changed whatever we want. eg.our logo)
    help_embed.set_thumbnail(url="https://emoji.gg/assets/emoji/3907_lol.png")

    help_embed.add_field(name="** **", value="** **", inline=False)

    help_embed.add_field(
        name="** **",
        value="**The list of command examples**",
        inline=False,
    )

    help_embed.add_field(
        name="** **",
        value=f"<@!{bot.user.id}> **{help_command.name}** \n {help_command.help}",
        inline=False,
    )

    for command in bot.commands:
        if not str(command).startswith("help"):
            help_embed.add_field(
                name="** **",
                value=f"<@!{bot.user.id}> **{command.name} summoner name** \n {command.help}",
                inline=False,
            )

    await ctx.send(embed=help_embed)


@bot.command(name="rank", help="Displays the information about the summoner.")
async def get_rank(ctx, name: str):
    """Sends the summoner's rank information to the bot"""
    try:
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


@bot.event
async def on_command_error(ctx, error):
    """Checks error and sends error message if exists"""
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")

    # Send an error message when the user input invalid command
    elif isinstance(error, commands.CommandNotFound):
        error = str(error)
        error = error[error.find('"') + 1 : error.rfind('"')]

        err_embed = discord.Embed(
            title=":warning:   Invalid Command",
            description=f"`{error}`  command is not a valid command.\n \
              \n Please type  `help`  to see how to use",
            color=discord.Color.orange(),
        )

        await ctx.send(embed=err_embed)


bot.run(TOKEN)
