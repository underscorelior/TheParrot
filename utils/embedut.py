import discord, asyncio
from discord.ext import commands
from discord_components import Button, ButtonStyle, Select, SelectOption
from discord.errors import HTTPException


class Reports(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx: commands.Context

    @commands.command(aliases=["r"])
    async def report(self, ctx):
        try:
            repmessage = await ctx.channel.fetch_message(
                ctx.message.reference.message_id
            )
            ch = ctx.guild.get_channel(808403507069059132)
            if repmessage.author.id == ctx.author.id:
                await ctx.author.send("You cant report yourself!")
                await ctx.message.delete()
            else:
                repsel = [
                    Select(
                        custom_id="repsel",
                        placeholder="Please select a report reason",
                        min_values=1,
                        max_values=4,
                        options=[
                            SelectOption(
                                emoji="🤬", label="Swearing/Bad Language", value="S"
                            ),
                            SelectOption(emoji="🔞", label="NSFW/Gore", value="N"),
                            SelectOption(emoji="⚠️", label="Toxicity", value="T"),
                            SelectOption(emoji="♻️", label="Repost/Stolen", value="R"),
                            SelectOption(emoji="🥩", label="Spam/Chat Flood", value="F"),
                            SelectOption(emoji="😡", label="Racism/Sexism", value="B"),
                        ],
                    )
                ]
                message = await ctx.send(
                    content=f"Reporting {repmessage.author} \nPlease select a reason!",
                    components=repsel,
                )

                def check(res):
                    return (
                        res.user.id == ctx.author.id
                        and res.channel.id == ctx.channel.id
                        and res.message.id == message.id
                    )

                try:
                    interaction = await self.bot.wait_for(
                        "select_option", check=check, timeout=30
                    )
                except asyncio.TimeoutError:
                    await message.delete()
                    await ctx.message.delete()
                    return await ctx.author.send(content="Timed out!")
                repcon = [
                    [
                        Button(emoji="✅", style=ButtonStyle.green, custom_id="y"),
                        Button(emoji="⛔", style=ButtonStyle.red, custom_id="n"),
                    ]
                ]
                await message.edit(
                    content="Are you sure you want to submit the report?",
                    components=repcon,
                )
                try:
                    conin = await self.bot.wait_for(
                        "button_click",
                        check=lambda inter: inter.message.id == message.id,
                        timeout=30,
                    )
                except asyncio.TimeoutError:
                    await message.delete()
                    await ctx.message.delete()
                    return await ctx.author.send(content="Timed out!")
                if conin.custom_id == "y":
                    repcat = ""
                    if "S" in interaction.values:
                        repcat += "🤬 Swearing/Bad Language    "
                    if "N" in interaction.values:
                        repcat += "🔞 NSFW/GORE    "
                    if "T" in interaction.values:
                        repcat += "⚠️ Toxicity    "
                    if "R" in interaction.values:
                        repcat += "♻️ Repost/Stolen    "
                    if "F" in interaction.values:
                        repcat += "🥩 Spam/Chat Flood    "
                    if "B" in interaction.values:
                        repcat += "😡 Racism/Sexism"
                    try:
                        imgs = repmessage.attachments[0].url
                        print(imgs)
                    except IndexError:
                        imgs = None
                    await conin.send("Sending report!")
                    await message.delete()
                    modsel = [
                        [
                            Button(
                                emoji="✅",
                                label="No Action",
                                style=ButtonStyle.green,
                                custom_id="f",
                            ),
                            Button(
                                emoji="⛔",
                                label="Delete and Warn",
                                style=ButtonStyle.red,
                                custom_id="w",
                            ),
                            Button(
                                emoji="🗑️",
                                label="Delete",
                                style=ButtonStyle.blue,
                                custom_id="d",
                            ),
                        ]
                    ]
                    await ctx.message.delete()
                    try:
                        embed = (
                            discord.Embed(
                                title=f"{repmessage.author} was reported!",
                                description=repmessage.content,
                                color=0xD42121,
                                url=repmessage.jump_url,
                            )
                            .set_image(url=imgs)
                            .set_author(
                                name=f"Reported by {ctx.author}",
                                icon_url=ctx.author.avatar_url,
                            )
                            .set_footer(text=f"Report categories: {repcat}")
                        )
                        repmods = await ch.send(embed=embed, components=modsel)
                    except HTTPException:
                        embed = (
                            discord.Embed(
                                title=f"{repmessage.author} was reported!",
                                description=repmessage.content,
                                color=0xD42121,
                                url=repmessage.jump_url,
                            )
                            .set_author(
                                name=f"Reported by {ctx.author}",
                                icon_url=ctx.author.avatar_url,
                            )
                            .set_footer(text=f"Report categories: {repcat}")
                        )
                        repmods = await ch.send(embed=embed, components=modsel)
                    repmodct = await self.bot.wait_for(
                        "button_click",
                        check=lambda inter: inter.message.id == repmods.id,
                    )
                    if repmodct.custom_id == "d":
                        for row in modsel:
                            row.disable_components()
                            await repmods.edit(
                                content=f"Message deleted. \nActioned by {repmodct.author}",
                                components=modsel,
                            )
                            await repmessage.delete()
                            await ctx.author.send("Your report has been dealt with.")
                    if repmodct.custom_id == "f":
                        for row in modsel:
                            row.disable_components()
                            await repmods.edit(
                                content=f"No Action. \nActioned by {repmodct.author}",
                                components=modsel,
                            )
                            await ctx.author.send("Your report has been dealt with.")
                    if repmodct.custom_id == "w":
                        for row in modsel:
                            row.disable_components()
                            await repmods.edit(
                                content=f"Deleted and Warned. \nActioned by {repmodct.author}",
                                components=modsel,
                            )
                            await ctx.author.send("Your report has been dealt with.")
                            await repmessage.delete()
                            await repmessage.author.send(
                                f"Your post in <#{repmessage.channel.id}> has been deleted for: \n{repcat}"
                            )
                else:
                    await conin.send("Cancelling report.")
                    await message.delete()
                    await ctx.message.delete()
        except AttributeError:
            await ctx.author.send('Please "reply" to another users message.')
            await ctx.message.delete()


def setup(bot):
    bot.add_cog(Reports(bot))
