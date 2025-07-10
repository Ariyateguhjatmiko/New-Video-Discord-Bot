import discord
import asyncio
import feedparser
from discord.ext import commands

# ===== CONFIG =====
TOKEN = 'MTM4NTc5Mjg5NTA0MjMyNjY0MQ.GdGTgm.B34TgmcXvRGCtYi8yICr3CfzM8Wxz46KuVq5tc'
CHANNEL_ID = 1385556607726911648  # ID channel Discord tujuan
YOUTUBE_RSS = 'https://www.youtube.com/feeds/videos.xml?channel_id=UCGDirlA9l0kz9MPuZGVsYMA'

# ===== SETUP BOT =====
intents = discord.Intents.default()
intents.message_content = True  # WAJIB agar bisa baca pesan user

bot = commands.Bot(command_prefix="!", intents=intents)

latest_video = None
chanel = None

# ===== FUNCTION KIRIM EMBED VIDEO =====
async def kirim_info_video(channel, video):
    video_id = video.link.split("v=")[-1] if "v=" in video.link else video.link.split("/")[-1]
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

    embed = discord.Embed(
        title=video.title,
        url=video.link,
        description="📢 Video baru telah diunggah!",
        color=discord.Color.red()
    )
    embed.set_thumbnail(url=thumbnail_url)
    await channel.send(embed=embed)

# ===== CEK YOUTUBE OTOMATIS =====
async def check_youtube(channel):
    global latest_video
    
    await bot.wait_until_ready()

    while not bot.is_closed():
        try:
            feed = feedparser.parse(YOUTUBE_RSS)
            if feed.entries:
                video = feed.entries[0]
                if latest_video != video.id:
                    latest_video = video.id
                    await kirim_info_video(channel, video)
        except Exception as e:
            print(f"❌ Gagal cek RSS: {e}")
        await asyncio.sleep(300)

# ===== EVENT SAAT BOT SIAP =====
@bot.event
async def on_ready():
    global chanel
    
    print(f'✅ Bot login sebagai {bot.user}')
    try:
        chanel = await bot.fetch_channel(CHANNEL_ID)
        print(f"📢 Channel ditemukan: {chanel}")
        bot.loop.create_task(check_youtube(chanel))
    except Exception as e:
        print(f"❌ Gagal ambil channel: {e}")

# ===== COMMAND !sendvideoinfo =====
@bot.command()
async def sendvideoinfo(ctx):
    try:
        feed = feedparser.parse(YOUTUBE_RSS)
        if feed.entries:
            video = feed.entries[0]
            await kirim_info_video(chanel, video)
        else:
            await ctx.send("Tidak ada video ditemukan.")
    except Exception as e:
        await ctx.send(f"Gagal ambil video: {e}")

# ===== JALANKAN BOT =====
bot.run(TOKEN)
