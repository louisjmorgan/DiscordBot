from dotenv import load_dotenv
import os
import shutil
from collections import deque

import youtube_dl

import discord
from discord.ext import commands
fromed discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
BOT_PREFIX = '!'

bot = commands.Bot(command_prefix=BOT_PREFIX)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )


@bot.command(name='cunt', help='fucks your cunt')
async def cuntfuck(ctx):
    response = 'fuck'
    await ctx.send(response)


@bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    try:
        if voice is not None:
            return await voice.move_to(channel)
        else:
            await channel.connect()

    except AttributeError:
        print('User is not connected to a voice channel')
        return await ctx.send(f'You must be in a voice channel before {bot.user} can join')

    await ctx.send(f'Joined {channel}')


@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice is not None:
        await voice.disconnect()
        print(f'{bot.user} has left {channel}\n')
        await ctx.send(f'Left {channel}')
    else:
        print(f'{bot.user} Unable to leave {channel}\n')
        await ctx.send(f'Unable to leave {channel}')

queues = deque()


@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, *url: str):

    def activate_queue():
        Queue_infile = os.path.isdir('./Queue')
        q_length = len(queues)

        if Queue_infile is True and q_length != 0:
            title = queues.popleft()
            print(f"Playing {title}\n")
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(
                os.path.realpath("Queue") + "/" + f"{title}.mp3")
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.remove(file)
            shutil.move(song_path, main_location)
            voice.play(discord.FFmpegPCMAudio(f"{title}.mp3"),
                       after=lambda e: activate_queue())
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.5
            return title

        else:
            queues.clear()
            print('No songs in queue\n')

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and (voice.is_playing() or voice.is_paused():
        return await queue(ctx, *url)

    else:
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.remove(file)

        Queue_infile = os.path.isdir('./Queue')
        try:
            Queue_folder = './Queue'
            if Queue_infile is True:
                print('Removed old queue folder\n')
                queues.clear
                shutil.rmtree(Queue_folder)
        except:
            print('No queue folder\n')

        await ctx.send('Preparing download')

        await queue(ctx, *url)

        now_playing = activate_queue()

        await ctx.send(f'Playing: {now_playing}')


@ bot.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print('Music paused\n')
        voice.pause()
        await ctx.send('Music Paused')
    else:
        print('Music not playing')
        await ctx.send('Music not playing - pause failed')


@ bot.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music\n")
        voice.resume()
        await ctx.send('Resumed music')

    else:
        print("Music not paused")
        await ctx.send("Music is not paused")


@ bot.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    queues.clear()

    queue_infile = os.path.isdir('./Queue')
    if queue_infile is True:
        shutil.rmtree('./Queue')

    if voice and voice.is_playing():
        print('Music stopped\n')
        voice.stop()
        await ctx.send('Music stopped')
    else:
        print('Music not playing\n')
        await ctx.send('Music not playing - stop failed')


@ bot.command(pass_context=True, aliases=['q', 'que'])
async def queue(ctx, *url: str):

    Queue_infile = os.path.isdir('./Queue')
    if Queue_infile is False:
        os.mkdir('Queue')

    print(f'{url}')

    if not url:
        list_queue = list(enumerate(queues, 1))
        string_queue = "\n".join(map(str, list_queue))
        return await ctx.send(f"{string_queue}")

    else:
        queue_path = os.path.abspath(
            os.path.realpath('Queue') + '/%(title)s.%(ext)s')

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': queue_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        song_search = " ".join(url)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('Downloading audio\n')

            track_info = ydl.extract_info(
                f"ytsearch1:{song_search}", download=True)
            track_info = track_info['entries'][0]

            title = ydl.prepare_filename(track_info)
            title = os.path.basename(title)
            title = os.path.splitext(title)[0]
            queues.append(title)
            print(f'Downloaded {title}\n')

        await ctx.send(f'Added {title} to the queue')
        print('Song added to queue\n')


@ bot.command(pass_context=True, aliases=['n', 'nex'])
async def next(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print('Playing next song\n')
        voice.stop()
        await ctx.send('Next song')
    else:
        print('Music not playing')
        await ctx.send('Music not playing - next failed')

bot.run(TOKEN)
