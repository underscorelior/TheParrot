import discord
import os
import time
from discord.utils import get
from discord.ext import commands
# from discord_components import DiscordComponents
from utils import userembed, waitembed, infoembed, modembed
from dotenv import load_dotenv
import markovify

bot = commands.Bot(
    command_prefix=["p-", "P-"],
    intents=discord.Intents.all(),
    status=discord.Status.idle,
    activity=discord.Game(name="With The Bread Pirate's crackers.")
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} at {time.ctime()}")
    await bot.load_extension("jishaku")
    await bot.load_extension("cogs.countries")
    # await bot.load_extension("cogs.quiz")
    await bot.load_extension("cogs.moderation")
    await bot.load_extension("cogs.eval")

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    ctx, guild, user = (
        await bot.get_context(message),
        bot.get_guild(722086066596741144),
        message.author,
    )
    if (
        not isinstance(message.channel, discord.DMChannel)
        or message.author.id == bot.user.id
    ):
        if ctx.channel.category_id == 809144803749134357:
            userid = int(ctx.channel.topic)
            mod = message.author
            dmuser = bot.get_user(userid)
            if message.content.startswith("-r") and mod.id != 808400358317490236:
                msg = str(message.content).replace("-r", "")
                await modembed(ctx, dmuser, msg, message)
    else:
        channelname, cate, channel = (
            str(ctx.author).replace("#", "-").replace(" ", "-").lower(),
            bot.get_channel(809144803749134357),
            get(guild.text_channels, topic=str(message.author.id)),
        )
        if not channel:
            channel = await guild.create_text_channel(name=channelname, category=cate, topic=message.author.id)
            await infoembed(message, channel, guild)
            await waitembed(user, message)
            await userembed(user, message, channel)
        else:
            await userembed(user, message, channel)

@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def breadspeak(ctx):
    if ctx.channel.id == 899886160204156928:
        try:
            await ctx.send(markovify.Text(open("dataset.txt", encoding="utf-8").read()).make_short_sentence(140))
        except Exception as e:
            await ctx.reply(e)

load_dotenv()
token = os.environ.get("TOKEN")
bot.run(token)