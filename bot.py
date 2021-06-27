import os
from dotenv import load_dotenv

# Discord
import discord
from discord.ext import commands

# Riot util func.
from riot import getSummonerRank, previousMatch

# saving df to image
import dataframe_image as dfi

dict = {
    "user": 123,
    "test": 123,
}


intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# TODO: Update prefix to be called with bot name.
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.event
async def on_member_join(member):
    # create a direct message channel.
    await member.create_dm()
    # Send welcome msg.
    await member.dm_channel.send(f"Hi {member.name}, welcome to 관전남 월드!")


@bot.command(name="rank", help="Get rank of summoner")
async def get_rank(ctx, name: str):
    embed = discord.Embed(title="Rank", description=getSummonerRank(name))
    await ctx.send(embed=embed)


@bot.command(name="last_match", help="Get last match history")
async def get_last_match(ctx, name: str):
    df = previousMatch(name)
    dfi.export(df, "df_styled.png")
    file = discord.File("df_styled.png")
    embed = discord.Embed()
    embed.set_image(url="attachment://df_styled.png")
    await ctx.send(embed=embed, file=file)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")


bot.run(TOKEN)
