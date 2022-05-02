import discord
import youtube_dl
from discord.ext import commands

# we can share these across commands like /play, /queue, /add, w.e
# if you wanna go overkill you can put these in a constants.py file
FFMPEG_OPTIONS = {
  'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
  'options':'-vn'
}

YDL_OPTIONS = {
  'format': 'bestaudio'
}

class music(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  ### CHECK: author_in_voice ###
  async def author_in_voice(ctx: commands.Context):
    result = ctx.author.voice and ctx.author.voice.channel
    if not result:
      await ctx.send('You must be in a voice channel to use this command.')
    return result

  ### CHECK: bot_is_playing ###
  async def bot_is_playing(ctx: commands.Context):
    result = ctx.voice_client and ctx.voice_client.is_playing()
    if not result:
      await ctx.send('Bot must be playing to use this command.')
    return result

  ### COMMAND: /play ###
  @commands.command()
  @commands.check(author_in_voice)
  async def play(self, ctx: commands.Context, ytUrl: str):
    # Connect to or move to author's current voice channel
    if not ctx.voice_client:
      await ctx.author.voice.channel.connect()
    elif ctx.voice_client.channel != ctx.author.voice.channel:
      await ctx.voice_client.move_to(ctx.author.voice.channel)

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(ytUrl, download=False)
      url = info['formats'][0]['url']
      source = discord.FFmpegOpusAudio(url, **FFMPEG_OPTIONS)

    if ctx.voice_client.is_playing():
      await ctx.send('Another song is still playing.')
    else:
      ctx.voice_client.play(source)
  
  ### COMMAND: /pause ###
  @commands.command()
  @commands.check(author_in_voice)
  @commands.check(bot_is_playing)
  async def pause(self, ctx: commands.Context):
    ctx.voice_client.pause()

  ### COMMAND: /resume ###
  @commands.command()
  @commands.check(author_in_voice)
  async def resume(self, ctx: commands.Context):
    if not ctx.voice_client or not ctx.voice_client.source:
      await ctx.send('Bot must be playing a song to pause.')
      return
    ctx.voice_client.resume()

  ### COMMAND: /leave ###
  @commands.command()
  @commands.check(author_in_voice)
  async def leave(self, ctx: commands.Context):
    if not ctx.voice_client:
      await ctx.send('Bot is not in a voice channel.')
      return

    await ctx.voice_client.disconnect()

def setup(client):
  cog = music(client)
  client.add_cog(cog)
