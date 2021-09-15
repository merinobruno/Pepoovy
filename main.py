import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv('pepoovy.env')
import youtube_dl
import time
DISCORD_TOKEN = 'ODg3MDU2MzQyNDQ2MTEyNzgw.YT-lmA.vxmYKBCyci3o5sbIrP4UqYGfXKE'

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='-',intents=intents)


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


@bot.command(name='p', help='To play song')
async def play(ctx,url):
    voice_client = ctx.message.guild.voice_client
    try:
        if voice_client.is_connected():
            try :
                server = ctx.message.guild
                voice_channel = server.voice_client

                async with ctx.typing():
                    filename = await YTDLSource.from_url(url, loop=bot.loop)
                    voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
                await ctx.send('**Now playing:** {}'.format(filename))
            except:
                ()
    except:
        if not ctx.message.author.voice:
                await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
                return
        else:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            try :
                server = ctx.message.guild
                voice_channel = server.voice_client


                filename = await YTDLSource.from_url(url, loop=bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
                await ctx.send('**Now playing:** {}'.format(filename))
            except:
                ()


@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()
    
    server = ctx.message.guild
    voice_channel = server.voice_client

    filename = await YTDLSource.from_url('https://www.youtube.com/watch?v=z6Uqf_Qo_e0', loop=bot.loop)
    voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))




@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    

@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use 'p [command]'")
    



@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    filename = await YTDLSource.from_url('https://www.youtube.com/watch?v=79LxziRFl9Q', loop=bot.loop)

    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        time.sleep(5.5)
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")




@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot.event
async def on_ready():
    print('Running!')
    for guild in bot.guilds:
        for channel in guild.text_channels :
            if str(channel) == "pepoovy" :
                await channel.send('I CAME!')

@bot.event
async def close():
    print('Shutting Down!')
    for guild in bot.guilds:
        for channel in guild.text_channels :
            if str(channel) == "pepoovy" :
                await channel.send('ded')


@bot.command()
async def a(ctx):
    text = "**a**"
    await ctx.send(text)

@bot.command()
async def quiensos(ctx):
    text = "**PARA UN POCO**"
    await ctx.send(text)

if __name__ == "__main__" :
    bot.run(DISCORD_TOKEN)