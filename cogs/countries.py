import asyncio
from datetime import UTC, datetime
import random
import aiohttp
import discord
from discord.ext import commands, tasks

from utils import (
    CAPITALS,
    CHANNEL_ID,
    COUNTRY,
    FLAGS,
    no_answer_embed,
    parse,
    # TERRITORY,
    starting_embed,
    update_score,
    win_embed,
    leaderboard,
)


class Countries(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.countries.start()

    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx: commands.Context[commands.Bot]):
        if ctx.channel.id == 954557457131266059 or ctx.channel.id == 955169257711370280:
            embed = leaderboard()

            await ctx.send(embed=embed)

    @tasks.loop(seconds=15)
    async def countries(self):
        channel: discord.guild.GuildChannel = self.bot.get_channel(CHANNEL_ID)
        last_message = False
        for message in [x async for x in channel.history(limit=5, oldest_first=False)]:
            if message and message.author.id != self.bot.user.id:
                last_message = True
                break
        if last_message:
            start_time = datetime.now(UTC).timestamp()

            # if not random.randint(0, 20):
            #     state_type = TERRITORY
            #     async with aiohttp.ClientSession() as session:

            #         async with session.get(
            #             "https://komali.dev/bin/territories.json", ssl=False
            #         ) as r:
            #             data = await r.json()
            # else:
            state_type = COUNTRY
            async with aiohttp.ClientSession() as session:

                async with session.get(
                    "https://geography.underscore.wtf/countries.json", ssl=False
                ) as r:
                    data = await r.json()
            answer_dict = random.choice(data)
            question_type = CAPITALS if random.randint(0, 1) else FLAGS

            answer = answer_dict["capital" if question_type == CAPITALS else "name"]

            if isinstance(answer, str):
                answer = [parse(answer)]
            else:
                answer = [parse(x) for x in answer]

            embed = starting_embed(answer_dict, question_type, state_type)

            game = await channel.send(embed=embed)

            def validate_message(message: discord.Message):
                if message.channel.id == CHANNEL_ID:
                    if message.author.id != self.bot.user.id:
                        answer_content = parse(message.content).split(" ")

                        for word in answer_content:
                            if word in answer:
                                return True

                return False

            try:
                message = await self.bot.wait_for(
                    "message", timeout=12.5, check=validate_message
                )
            except asyncio.TimeoutError:
                embed = no_answer_embed(answer_dict, question_type, state_type)
                await game.edit(embed=embed)
            else:
                await message.add_reaction("✅")
                player_score = update_score(message.author.id)

                embed = win_embed(
                    answer_dict,
                    question_type,
                    state_type,
                    message.author,
                    player_score,
                    start_time,
                )

                await game.edit(embed=embed)

    def cog_unload(self):
        self.countries.cancel()

    @countries.before_loop
    async def before_countries(self):
        print("Starting")
        await self.bot.wait_until_ready()
        print("Started")


async def setup(bot):
    await bot.add_cog(Countries(bot))
