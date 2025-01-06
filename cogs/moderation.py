from discord.ext import commands
import discord

PIRATE_ROLE_ID = 1169433827530260481


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx: commands.Context

    # @commands.command(aliases=["strike"])
    # @commands.has_any_role("Moderator")
    # async def warn(self, ctx, id: discord.Member, *, reason):
    #     embed = discord.Embed(title="Strike", color=0xFF0000)
    #     embed.set_author(
    #         name="The Bread Pirate",
    #         icon_url="https://cdn.discordapp.com/attachments/808448077614415882/837336840272609290/Better_bread_server.gif",
    #     )
    #     embed.add_field(name="You have been warned for:", value=reason)
    #     embed.set_footer(text="If you think this was an error, reply to this message!")
    #     await id.send(embed=embed)
    #     await ctx.send(content=f"{id.name} was warned:", embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.nick == after.nick:
            return

        if "pirate" in after.nick.lower():
            if PIRATE_ROLE_ID in [role.id for role in before.roles]:
                return
            else:
                await after.add_roles(
                    after.guild.get_role(PIRATE_ROLE_ID),
                    reason='Added "Pirate" to nickname',
                )
        else:
            if "pirate" in before.nick.lower():
                if PIRATE_ROLE_ID in [role.id for role in before.roles]:
                    await after.remove_roles(
                        after.guild.get_role(PIRATE_ROLE_ID),
                        reason='Removed "Pirate" from nickname',
                    )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await member.add_roles(member.guild.get_role(722089620099170384))

        if "pirate" in member.display_name.lower():
            await member.add_roles(
                member.guild.get_role(PIRATE_ROLE_ID),
                reason='Joined with "Pirate" in username',
            )


async def setup(bot):
    await bot.add_cog(Moderation(bot))
