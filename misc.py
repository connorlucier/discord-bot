import discord
from discord.ext import commands

class Misc(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client
  
  ### LISTENER: on_message ###
  @commands.Cog.listener('on_message')
  async def reply_with_HUH(self, message: discord.Message):
    # Ignore messages sent by the bot
    if message.author == self.client.user:
      return

    # Reply with 'HUH' if mentioned
    if self.client.user.mentioned_in(message):
      HUH_emoji = discord.utils.get(self.client.emojis, name='HUH')
      if HUH_emoji is not None:        
        await message.channel.send(str(HUH_emoji))

    # Add a reaction when someone batchests
    BAT_emoji = self.get_emoji('BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAT')
    if BAT_emoji is not None and str(BAT_emoji) in message.content:
      await message.add_reaction(BAT_emoji)

    # React with FROMARCANE when someone mentions a character from the show
    from_arcane = ['powder', 'jinx', 'vi', 'jayce', 'caitlyn', 'ekko', 'silco', 'heimer', 'viktor']
    has_character = len([True for char in from_arcane if char in message.content.lower()]) > 0
    if has_character:
      FROMARCANE_emoji = self.get_emoji('FROMARCANE')
      await message.add_reaction(FROMARCANE_emoji)

  ### COMMAND: /bozo ###
  @commands.command()
  async def bozo(self, ctx: commands.Context, username=None):
    url = 'https://media.tenor.com/images/d5ac2e0b3c909508e230aa5b63ee24f8/tenor.gif'
    desc = "Get BOZO'd son" if username is None else f'{username} is a BOZO'
    img = discord.Embed(title='RIPBOZO', description=desc)
    img.set_image(url=url)
    await ctx.send(embed=img)

  ### HELPER: get_emoji ###
  def get_emoji(self, emoji_name: str):
    return discord.utils.get(self.client.emojis, name=emoji_name)

def setup(client):
  cog = Misc(client)
  client.add_cog(cog)
