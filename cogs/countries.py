import asyncio
import json
import random
from datetime import datetime
from re import sub

import aiohttp
import discord
from discord.ext import commands, tasks
from discord.utils import get
from unidecode import unidecode

global xpgain
with open("utils/xpgain.txt", "r") as f:
	xpgain = int(f.read())

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

def _parse_(content: str) -> str:
	_c_ = sub("[^a-zA-Z]", "", unidecode(content)).lower()
	return _c_.strip()


shortdict = {
	# countries
	"unitedstates": "usa",
	"unitedkingdom": "uk",
	"unitedarabemirates": "uae",
	"northkorea": "nk",
	"southkorea": "sk",
	"newzealand": "nz",
	"republicofthecongo": "roc",
	"drcongo": "drc",
	"dominicanrepublic": "dr",
	"saintvincentandthegrenadines": "svg",
	"papuanewguinea": "png",
	"antiguaandbarbuda": "ab",
	"saudiarabia": "sa",
	"trinidadandtobago": "tt",
	"bosniaandherzegovina": "bh",
	"saotomeandprincipe": "stp",
	"saintkittsandnevis": "skn",
	"centralafricanrepublic": "car",
	"guineabissau": "gb",
	"timorleste": "tl",
	"northmacedonia": "nm",
	"france": "bad",
	# territories
	"newcaledonia": "nc",
	"sainthelena": "sh",
	"saintpierreandmiquelon": "spm",
	"britishindianoceanterritory": "biot",
	"cocoskeelingislands": "cki",
	"northernmarianaislands": "nmi",
	"turksandcaicosislands": "tci",
	"britishvirginislands": "bvi",
	"usvirginislands": "uvi",
	"frenchpolynesia": "fp",
	"saintbarthelemy": "sb",
	"americansamoa": "as",
	# capitals
	"washingtondc": "dc",
	# secondary spellings
	"ulaanbaatar": "ulanbator",
	"macao": "macau",
}


class Countries(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.countries.start()
	@commands.command(aliases=["lb"])
	async def leaderboard(self, ctx):
		if ctx.channel.id == 954557457131266059 or ctx.channel.id == 955169257711370280:
			with open("quizlb.json", "r") as f:
				data = json.load(f)
			top_users = {
				k: v
				for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)
			}
			names = ""
			for postion, user in enumerate(top_users):
				names += f"{postion+1} - <@!{user}> | {top_users[user]}\n"
			embed = discord.Embed(title="Leaderboard")
			embed.add_field(name="Names", value=names, inline=False)
			await ctx.send(embed=embed)

	@tasks.loop(seconds=15)
	async def countries(self):
		guild=self.bot.get_guild(722086066596741144)
		channel = get(guild.text_channels, topic=str("Country quiz, new game starts every 15 seconds! https://github.com/underscorelior/TheParrot"))
		for message in [x async for x in channel.history(limit=15, oldest_first=False)]:
			if message.author.id != self.bot.user.id:
				msgtime = message.created_at.timestamp()
				print((int(datetime.utcnow().timestamp())-int(msgtime))-25200)
				break
		if (int(datetime.utcnow().timestamp())-int(msgtime))-25200 <= 60:
			async with aiohttp.ClientSession() as session:
				async with session.get("https://underscore.wtf/countries/countries.json", ssl=False) as r:
					data = await r.json()
				async with session.get("https://komali.dev/bin/territories.json", ssl=False ) as f:
					altdata = await f.json()
			t = random.randint(1, 2)
			quizans = data[random.randint(0, len(data) - 1)]
			if t == 1 and quizans["capital"]:
				t = "capital"
				startemb = discord.Embed(
					title=f'What is the capital of `{quizans["name"]}`?',
					color=0x1860CC,
					timestamp=datetime.utcnow(),
				)
			else:
				if random.randint(1, 17) == 7:
					quizans = altdata[random.randint(0, len(altdata) - 1)]
					tc = 1
				else:
					tc = 2
				t = "name"
				startemb = discord.Embed(
					title=f'Which {"country" if tc==2 else "territory"} does this flag belong to?',
					color=0x1860CC,
					timestamp=datetime.utcnow(),
				).set_image(url=quizans["flags"])
			em = await channel.send(embed=startemb)
			ans = quizans[t]

			if isinstance(ans, str):
				ans = [_parse_(ans)]
			else:
				ans = [_parse_(x) for x in ans]

			def check(message: discord.Message) -> bool:
				content = _parse_(message.content)
				for sh in ans:
					if sh in shortdict.keys():
						cnt = shortdict[sh]
					else:
						cnt = sh
				check1 = message.channel == channel and message.author != self.bot
				check2 = content in ans or content == cnt
				return check1 and check2

			try:
				message = await self.bot.wait_for("message", timeout=12.5, check=check)
			except asyncio.TimeoutError:
				if t == "capital":
					await em.edit(
						embed=discord.Embed(
							title="No one answered correctly!",
							description=f'What is the capital of `{quizans["name"]}`: \nAnswer: `{quizans["capital"] if isinstance(quizans["capital"], str) else "/".join(quizans["capital"])}`',
							color=0xFA8E23,
							timestamp=datetime.utcnow(),
						)
					)  #
				else:
					await em.edit(
						embed=discord.Embed(
							title="No one answered correctly!",
							description=f'Which {"country" if tc==2 else "territory"} does this flag belong to?: \nAnswer: `{quizans["name"] if isinstance(quizans["name"], str) else "/".join(quizans["name"])}`',
							color=0xFA8E23,
							timestamp=datetime.utcnow(),
						).set_thumbnail(url=quizans["flags"])
					)
			else:
				with open("quizlb.json", "r+") as f:
					data = json.load(f)
				if str(message.author.id) not in points.keys():
					points[str(message.author.id)] = xpgain
					_save()
				else:
					points[str(message.author.id)] += xpgain
					_save()
				totals = points[str(message.author.id)]
				if totals == 1000:
					if str(message.author.mobile_status).lower() != "offline":
						await message.author.send(
							embed=discord.Embed(
								title=f"{message.author.name} congratulations on reaching 1000 xp!",
								description=f"You are now a geography nerd! You gain the @Oceanographer role, and achess to the Geography Nerds special channel which gives you access to on demand games of quizes.",
								color=0x9FEF2E,
								timestamp=datetime.utcnow(),
							)
						)
					else:
						await message.author.send("""
```ansi
You are officially a [1;33m[1;40mnerd![0m You gain the [1;34m[1;40m@Oceanographer role[0m, and access to the the [1;32m[1;40mGeography Nerds[0m special channel which gives you access to on demand games of quizes.	
```""")
					role = get(guild.roles, name="Oceanographers")
					member = guild.get_member(message.author.id)
					await member.add_roles(role)
					await self.bot.get_channel(808448077614415882).send(
						f"New <@&954556452087922730>! \nGGs to {message.author.mention} for getting 1000 countries/flags correct!"
					)
				await message.add_reaction("✅")
				if t == "capital":
					await em.edit(
						embed=discord.Embed(
							title=f"{message.author} answered correctly!",
							description=f'What is the capital of `{quizans["name"]}`: \nAnswer: `{quizans["capital"] if isinstance(quizans["capital"], str) else "/".join(quizans["capital"])}`',
							color=0x3CB556,
							timestamp=datetime.utcnow(),
						)
						.set_author(
							name=message.author, icon_url=message.author.avatar_url
						)
						.set_footer(text=f"They have a total of {totals} point(s)!")
					)
				else:
					await em.edit(
						embed=discord.Embed(
							title=f"{message.author} answered correctly!",
							description=f'Which {"country" if tc==2 else "territory"} does this flag belong to? \nAnswer: `{quizans["name"] if isinstance(quizans["name"], str) else "/".join(quizans["name"])}`',
							color=0x3CB556,
							timestamp=datetime.utcnow(),
						)
						.set_thumbnail(url=quizans["flags"])
						.set_author(
							name=message.author, icon_url=message.author.avatar_url
						)
						.set_footer(text=f"They have a total of {totals} point(s)!")
					)
			finally:
				print("Done")

	def cog_unload(self):
		self.countries.cancel()

	@countries.before_loop
	async def before_countries(self):
		print("Starting")
		await self.bot.wait_until_ready()
		print("Started")


def _save():
	with open("quizlb.json", "w+") as f:
		json.dump(points, f)


async def setup(bot):
	await bot.add_cog(Countries(bot))
