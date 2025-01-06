import discord
import os
import time
from discord.ext import commands

from dotenv import load_dotenv

bot = commands.Bot(
    command_prefix=["p-", "P-"],
    intents=discord.Intents.all(),
    status=discord.Status.idle,
    activity=discord.Game(name="With The Bread Pirate's crackers."),
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} at {time.ctime()}")
    await bot.load_extension("jishaku")
    await bot.load_extension("cogs.countries")
    # await bot.load_extension("cogs.purge")
    await bot.load_extension("cogs.reload")
    await bot.load_extension("cogs.moderation")


load_dotenv()
token = os.environ.get("TOKEN")
bot.run(token)
