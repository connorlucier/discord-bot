import os
import discord, misc, music
from discord.ext import commands
from keep_alive import keep_alive

cmd_prefix = '/'
intents = discord.Intents.all()
client = commands.Bot(cmd_prefix, intents=intents, case_insensitive=True)
cogs = [misc, music]

for cog in cogs:
  cog.setup(client)

keep_alive()
client.run(os.environ['botSecretKey'])
