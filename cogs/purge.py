import datetime
import time
from discord.ext import commands
import discord


class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx: commands.Context

    @commands.command()
    @commands.has_any_role("Moderator")
    async def purge(self, ctx: commands.Context):
        after = datetime.datetime.fromtimestamp(time.time()) - datetime.timedelta(
            days=30
        )

        valid_roles = [
            722089586641076377,
            954556452087922730,
            954556214530941038,
            808463326346477589,
            722089765268226058,
            808464764593897512,
        ]

        all_ids = {
            user.id: user
            for user in ctx.guild.members
            if not any(role.id in valid_roles for role in user.roles)
        }

        for channel in ctx.guild.text_channels:
            async for msg in channel.history(after=after, limit=None):
                all_ids.pop(msg.author.id, None)

        for member in list(all_ids.values()):
            try:
                await member.kick()
                await ctx.send(f"Kicked {member.name}")
            except discord.Forbidden:
                print(f"Errored {member.name}")

        await ctx.send(f"Successfully kicked {len(list(all_ids.values()))} members")


async def setup(bot):
    await bot.add_cog(Purge(bot))
