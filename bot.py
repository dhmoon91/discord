import os
from dotenv import load_dotenv

# Discord
import discord
from discord.ext import commands

# Riot util func.
from riot import getSummonerRank,previousMatch

# saving df to image
import dataframe_image as dfi


intents = discord.Intents.default()
intents.members = True # Subscribe to the privileged members intent.

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# TODO: Update prefix to be called with bot name.
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
  # create a direct message channel.
  await member.create_dm()
  # Send welcome msg.
  await member.dm_channel.send(
      f'Hi {member.name}, welcome to 관전남 월드!'
  )

@bot.command(name='rank', help='Get rank of summoner')
async def get_rank(ctx, name:str):
  summoner_info = getSummonerRank(name)

  embed = discord.Embed(title = "Solo/Duo Rank", color = discord.Color.dark_gray())

  summoner_name = summoner_info['user_name']
  
  # Add author, thumbnail, fields, and footer to the embed
  embed.set_author(name=summoner_name, url=f"https://na.op.gg/summoner/userName={summoner_name}", icon_url=summoner_info['summoner_icon_image_url'])
  
  # Get image of tier by path
  tier_image = summoner_info['tier_image']
  file = discord.File(tier_image)
  # Need to get the filename in order to attach to the thumbnail
  tier_image_filename = tier_image.replace('ranked-emblems/', '')
  # Embed thumbnail image of tier at the side of the embed
  embed.set_thumbnail(url=f"attachment://{tier_image_filename}")

  # Setting variables for summoner information to display as field
  summoner_rank = summoner_info['tier']
  solo_win = summoner_info['solo_win']
  solo_loss = summoner_info['solo_loss']
  summoner_total_game = solo_win + solo_loss
  solo_rank_percentage = int(solo_win / summoner_total_game * 100)


  embed.add_field(name=summoner_rank, 
  value=f"Total Games Played: {summoner_total_game}\n{solo_win}W {solo_loss}L {solo_rank_percentage}%", 
  inline=False)
  await ctx.send(file=file, embed = embed)

@bot.command(name='last_match', help='Get last match history')
async def get_last_match(ctx, name:str):
  df = previousMatch(name)
  dfi.export(df, 'df_styled.png')
  file = discord.File("df_styled.png")
  embed = discord.Embed()
  embed.set_image(url="attachment://df_styled.png")
  await ctx.send(embed=embed, file=file)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
bot.run(TOKEN)