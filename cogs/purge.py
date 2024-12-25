from discord.ext import commands
import discord


class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx: commands.Context


async def setup(bot):
    await bot.add_cog(Purge(bot))