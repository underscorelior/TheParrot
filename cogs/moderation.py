from discord.ext import commands
import discord


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx: commands.Context

    @commands.command(aliases=["strike"])
    @commands.has_any_role("Moderator")
    async def warn(self, ctx, id: discord.Member, *, reason):
        embed = discord.Embed(title="Strike", color=0xFF0000)
        embed.set_author(
            name="The Bread Pirate",
            icon_url="https://cdn.discordapp.com/attachments/808448077614415882/837336840272609290/Better_bread_server.gif",
        )
        embed.add_field(name="You have been warned for:", value=reason)
        embed.set_footer(text="If you think this was an error, reply to this message!")
        await id.send(embed=embed)
        await ctx.send(content=f"{id.name} was warned:", embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))