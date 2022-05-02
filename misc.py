import discord
from discord.ext import commands

class misc(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client
  
  ### LISTENER: on_message ###
  @commands.Cog.listener()
  async def on_message(self, message: discord.Message):
      if message.author == self.client.user:
          return
      if self.client.user.mentioned_in(message):
        emoji = discord.utils.get(self.client.emojis, name='HUH')
        await message.channel.send(str(emoji))

  ### COMMAND: /bozo ###
  @commands.command()
  async def bozo(self, ctx: commands.Context, username=None):
    url = 'https://media.tenor.com/images/d5ac2e0b3c909508e230aa5b63ee24f8/tenor.gif'
    desc = "Get BOZO'd son" if username is None else f'{username} is a BOZO'
    img = discord.Embed(title='RIPBOZO', description=desc)
    img.set_image(url=url)
    await ctx.send(embed=img)

def setup(client):
  cog = misc(client)
  client.add_cog(cog)
