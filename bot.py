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
intents.members = True  # Subscribe to the privileged members intent.

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Update prefix to be called with bot name.
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)


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
    print(summoner_info["summoner_icon_image_url"])
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


@bot.event
async def on_command_error(ctx, error):
    """Checks error and sends error message if exists"""
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")


bot.run(TOKEN)
