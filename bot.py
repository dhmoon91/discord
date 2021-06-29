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
from riot import get_summoner_rank, previous_match, create_summoner_list

intents = discord.Intents.default()
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

    data_path = "data"
    data_file = "/inhouse_members.json"

    players_list = message.split(", ")
    players_list_info = create_summoner_list(players_list)

    if len(players_list) != 10:
        await ctx.send(
            f"You have just added {len(players_list)} number of players.\n"
            + f"You need to add {10 - len(players_list)} more!"
        )

    if not os.path.exists(data_path + data_file):
        pass
    else:
        pass

    embed = discord.Embed(title="List of Summoners", color=discord.Color.dark_gray())

    for count in range(len(players_list)):

        output_info = {
            "name": players_list_info["members"][count]["user_name"],
            "tier_accronym": players_list_info["members"][count]["tier_division"][0]
            + players_list_info["members"][count]["tier_rank_number"],
        }

        players_list_info["members"][count]["user_name"]
        embed.add_field(
            name="** **",
            value=output_info["tier_accronym"] + " " + output_info["name"],
            inline=False,
        )

    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    """Checks error and sends error message if exists"""
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")


bot.run(TOKEN)
