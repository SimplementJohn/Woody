import discord
from discord.ext import commands
import yt_dlp
import asyncio
import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

music_queue = []  # (ctx, url, title)
is_playing = False

inactivity_timeout = 15 * 60  # 15 minutes
timer_idle_seconds = 0

bot.uptime = datetime.datetime.now()

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user.name}")
    bot.loop.create_task(check_inactivity())

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"🔊 Connecté au salon : {channel.name}")
    else:
        await ctx.send("❌ Tu dois être dans un salon vocal !")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Déconnecté du salon vocal.")
    else:
        await ctx.send("❌ Je ne suis pas connecté à un salon vocal.")

@bot.command()
async def p(ctx, *, query):
    global is_playing
    
    if not ctx.voice_client:
        await ctx.invoke(bot.get_command("join"))

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'default_search': 'ytsearch1',
    }

    await ctx.send("🔎 Recherche de la musique...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ydl.extract_info(query, download=False))
        info = data['entries'][0] if 'entries' in data else data
        url = info['url']
        title = info['title']

    music_queue.append((ctx, url, title))
    await ctx.send(f"➕ Ajouté à la file : **{title}**")

    if not is_playing:
        await play_next()

async def play_next():
    global is_playing, timer_idle_seconds
    if music_queue:
        ctx, url, title = music_queue.pop(0)
        is_playing = True
        timer_idle_seconds = 0

        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        source = discord.FFmpegOpusAudio(url, **ffmpeg_options)

        def after_play(err):
            if err:
                print(f"Erreur lecture : {err}")
            fut = play_next()
            asyncio.run_coroutine_threadsafe(fut, bot.loop)

        ctx.voice_client.play(source, after=after_play)
        await ctx.send(f"🎶 Lecture de : **{title}**")
    else:
        is_playing = False

@bot.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭ Passage à la musique suivante...")
    else:
        await ctx.send("❌ Aucune musique à passer.")

@bot.command()
async def queue(ctx):
    if not music_queue:
        await ctx.send("📬 La file est vide.")
    else:
        lines = [f"{i+1}. {item[2]}" for i, item in enumerate(music_queue)]
        await ctx.send("\n".join(lines))

@bot.command()
async def stop(ctx):
    global is_playing
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        is_playing = False
        await ctx.send("⏹️ Musique arrêtée et bot déconnecté.")
    else:
        await ctx.send("❌ Pas connecté à un salon vocal.")

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Latence : {round(bot.latency * 1000)}ms")

@bot.command()
async def uptime(ctx):
    now = datetime.datetime.now()
    uptime = now - bot.uptime
    await ctx.send(f"⏱️ En ligne depuis {uptime}")

@bot.command()
async def settimeout(ctx, minutes: int):
    global inactivity_timeout
    inactivity_timeout = minutes * 60
    await ctx.send(f"⏲️ Timeout réglé sur {minutes} minutes")

async def check_inactivity():
    global timer_idle_seconds, is_playing
    await bot.wait_until_ready()
    while not bot.is_closed():
        for vc in bot.voice_clients:
            if not vc.is_playing():
                timer_idle_seconds += 60
            else:
                timer_idle_seconds = 0
        if timer_idle_seconds >= inactivity_timeout:
            for vc in bot.voice_clients:
                await vc.disconnect()
                print("⏲️ Déconnexion pour inactivité.")
            is_playing = False
            timer_idle_seconds = 0
        await asyncio.sleep(60)

bot.run(os.getenv("DISCORD_TOKEN"))
