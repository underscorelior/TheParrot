import asyncio
import json
import random
from datetime import datetime

import aiohttp
import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from utils import checkans, losebtn, toembed, toembedt, winbtn

global xpgain
with open("utils/xpgain.txt", "r") as f:
	xpgain = int(f.read())
	print(xpgain)

global points
try:
    with open("quizlb.json") as f:
        points = json.load(f)
        print("Successfully loaded quizlb.json")
except FileNotFoundError:
    print("Could not load quizlb.json, creating new file")
    with open("quizlb.json", "w") as f:
        f.write("{}")
    with open("quizlb.json") as f:
        points = json.load(f)

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["q"])
    async def quiz(self, ctx):
        if ctx.channel.id == 955169257711370280:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://underscore.wtf/countries/countries.json", ssl=False
                ) as r:
                    data = await r.json()
            quizans = data[random.randint(0, len(data) - 1)]
            ansloc = random.randint(1, 4)
            qtype = random.randint(1, 2)
            if qtype == 1:
                qt = "capital"
            else:
                qt = "name"
            ca = await checkans(data, ansloc, quizans, qt)
            btnans = [
                [
                    Button(label=ca[0], emoji="🇦", style=ButtonStyle.blue, custom_id=1),
                    Button(label=ca[1], emoji="🇧", style=ButtonStyle.blue, custom_id=2),
                    Button(label=ca[2], emoji="🇨", style=ButtonStyle.blue, custom_id=3),
                    Button(label=ca[3], emoji="🇩", style=ButtonStyle.blue, custom_id=4)
                ]
            ]
            if qtype == 1:
                msem = discord.Embed(
                    title=f'What is the capital of `{quizans["name"]}`:',
                    color=0x1860CC,
                    timestamp=datetime.utcnow(),
                ).set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            else:
                msem = (
                    discord.Embed(
                        title=f"Which country does this flag belong to?",
                        color=0x1860CC,
                        timestamp=datetime.utcnow(),
                    )
                    .set_image(url=quizans["flags"])
                    .set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                )
            message = await ctx.send(
                content=ctx.author.mention, embed=msem, components=btnans
            )
            try:
                ansch = await self.bot.wait_for(
                    "button_click",
                    check=lambda inter: inter.message.id == message.id
                    and inter.user.id == ctx.author.id,
                    timeout=15,
                )
            except asyncio.TimeoutError:
                if qtype == 1:
                    return await message.edit(
                        embed=await toembed(
                            f'What is the capital of `{quizans["name"]}`: \nAnswer: `{quizans["capital"]}`'
                        ),
                        components=[
                            [
                                Button(
                                    emoji="🇦", style=ButtonStyle.grey, disabled=True
                                ),
                                Button(
                                    emoji="🇧", style=ButtonStyle.grey, disabled=True
                                ),
                                Button(
                                    emoji="🇨", style=ButtonStyle.grey, disabled=True
                                ),
                                Button(
                                    emoji="🇩", style=ButtonStyle.grey, disabled=True
                                ),
                            ]
                        ],
                    )
                else:
                    return await message.edit(
                        embed=await toembedt(
                            f'Which country does this flag belong to? \nAnswer: `{quizans["name"]}`',
                            quizans["flags"],
                        ),
                        components=[
                            [
                                Button(
                                    emoji="🇦", style=ButtonStyle.grey, disabled=True
                                ),
                                Button(
                                    emoji="🇧", style=ButtonStyle.grey, disabled=True
                                ),
                                Button(
                                    emoji="🇨", style=ButtonStyle.grey, disabled=True
                                ),
                                Button(
                                    emoji="🇩", style=ButtonStyle.grey, disabled=True
                                ),
                            ]
                        ],
                    )
            if int(ansch.custom_id) == ansloc:
                with open("quizlb.json", "r+") as f:
                    data = json.load(f)
                points[str(ctx.author.id)] += xpgain
                _save()
                if qtype == 1:
                    await message.edit(
                        embed=discord.Embed(
                            title="Win",
                            description=f'What is the capital of `{quizans["name"]}`: \nAnswer: `{quizans["capital"]}`',
                            color=0x3CB556,
                            timestamp=datetime.utcnow(),
                        ).set_footer(
                            text=f"{ctx.author} | {points[str(ctx.author.id)]} Point(s)",
                            icon_url=ctx.author.avatar_url,
                        ),
                        components=await winbtn(ansloc),
                    )
                else:
                    await message.edit(
                        embed=discord.Embed(
                            title="Win",
                            description=f'Which country does this flag belong to? \nAnswer: `{quizans["name"]}`',
                            color=0x3CB556,
                            timestamp=datetime.utcnow(),
                        )
                        .set_footer(
                            text=f"{ctx.author} | {points[str(ctx.author.id)]} Point(s)",
                            icon_url=ctx.author.avatar_url,
                        )
                        .set_thumbnail(url=quizans["flags"]),
                        components=await winbtn(ansloc),
                    )
            else:
                qta = await losebtn(int(ansch.custom_id), ansloc)
                if qtype == 1:
                    await message.edit(
                        embed=discord.Embed(
                            title="Lose",
                            description=f'What is the capital of `{quizans["name"]}`: \nSelected Answer: `{btnans[0][qta[1]-1].label}` \nReal Answer: `{quizans["capital"]}`',
                            color=0xFA8E23,
                            timestamp=datetime.utcnow(),
                        ).set_footer(
                            text=f"{ctx.author} | {points[str(ctx.author.id)]} Point(s)",
                            icon_url=ctx.author.avatar_url,
                        ),
                        components=qta[0],
                    )
                else:
                    await message.edit(
                        embed=discord.Embed(
                            title="Lose",
                            description=f'Which country does this flag belong to? \nSelected Answer: `{btnans[0][qta[1]-1].label}` \nReal Answer: `{quizans["name"]}``',
                            color=0xFA8E23,
                            timestamp=datetime.utcnow(),
                        )
                        .set_footer(
                            text=f"{ctx.author} | {points[str(ctx.author.id)]} Point(s)",
                            icon_url=ctx.author.avatar_url,
                        )
                        .set_thumbnail(url=quizans["flags"]),
                        components=await winbtn(ansloc),
                    )


def _save():
    with open("quizlb.json", "w+") as f:
        json.dump(points, f)


def setup(bot):
    bot.add_cog(Quiz(bot))
