from discord.ext import tasks, commands
from discord.utils import get
import random
import aiohttp
import discord
from datetime import datetime
import asyncio
import json
import unidecode
global amounts
try:
	print("Successfully loaded amounts.json")
	with open('lb.json') as f:
		amounts = json.load(f)
except FileNotFoundError:
	print("Could not load amounts.json")
class Countries(commands.Cog):
	def __init__(self, bot):
		self.index = 0
		self.bot = bot
		self.countries.start()
	
	@commands.command(aliases=["lb"])
	async def leaderboard(self,ctx):
		guild=self.bot.get_guild(722086066596741144)
		channel = get(guild.text_channels, topic=str("Country quiz, new game starts every 15 seconds! https://github.com/underscorelior/TheParrot"))
		if channel.id == ctx.channel.id:
			with open('lb.json', 'r') as f:
				data = json.load(f)
			top_users = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}
			names = ''
			for postion, user in enumerate(top_users):
				names += f'{postion+1} - <@!{user}> | {top_users[user]}\n'
			embed = discord.Embed(title="Leaderboard")
			embed.add_field(name="Names", value=names, inline=False)
			await ctx.send(embed=embed)

	def cog_unload(self):
		self.countries.cancel()
	
	@tasks.loop(seconds=15)
	async def countries(self):
		guild=self.bot.get_guild(722086066596741144)
		channel = get(guild.text_channels, topic=str("Country quiz, new game starts every 15 seconds! https://github.com/underscorelior/TheParrot"))
		async for message in channel.history(limit=100,oldest_first=False):
			if message.author.id == 808400358317490236 or message.author.id == 954989125696618496:
				print("No")
			else:
				x= message.created_at.timestamp()
				break
		if (x-datetime.utcnow().timestamp()) <= -200:
			
			print("No one \n"+str(x-datetime.utcnow().timestamp()))
		else:
			t = random.randint(1,2)
			async with aiohttp.ClientSession() as session: 
				async with session.get("https://underscore.wtf/countries/countries.json", ssl=False) as r: data = await r.json()
			quizans=data[random.randint(0,len(data)-1)]
			ccfixed = unidecode.unidecode(quizans["capital"])
			nnfixed = unidecode.unidecode(quizans["name"])
			if t == 1:
				msem = discord.Embed(title=f'What is the capital of `{quizans["name"]}`:',color=0x1860cc, timestamp = datetime.utcnow())
			else:
				msem = discord.Embed(title=f'Which country does this flag belong to?',color=0x1860cc, timestamp = datetime.utcnow()).set_image(url=quizans["flags"])
			em = await channel.send(embed=msem)	
			if t == 1: 
				t="capital"
				if quizans["capital"] == "City of San Marino": qex="San Marino"
				else: qex=ccfixed
			else: 
				t="name"
				if quizans["name"] == "United States": qex="usa"
				elif quizans["name"] == "United Arab Emirates": qex="uae"
				elif quizans["name"] == "United Kingdom": qex="uk"
				elif quizans["name"] == "Afghanistan": qex="taliban"
				elif quizans["name"] == "Taiwan": qex="prc"
				elif quizans["name"] == "North Korea": qex="nk"
				elif quizans["name"] == "South Korea": qex="sk"
				elif quizans["name"] == "New Zealand": qex="nz"
				elif quizans["name"] == "Republic of the Congo": qex="roc"
				elif quizans["name"] == "DR Congo": qex="drc"
				elif quizans["name"] == "Dominican Republic": qex="dr"
				elif quizans["name"] == "Saint Vincent and the Grenadines": qex="svg"
				elif quizans["name"] == "Papua New Guinea": qex="png"
				elif quizans["name"] == "Antigua and Barbuda": qex="ab"
				elif quizans["name"] == "Sierra Leone": qex="sl"
				elif quizans["name"] == "Trinidad and Tobago": qex="tt"
				elif quizans["name"] == "Bosnia and Herzegovina": qex="bh"
				elif quizans["name"] == "Saint Kitts and Nevis": qex="skn"
				elif quizans["name"] == "São Tomé and Príncipe": qex="stp"
				elif quizans["name"] == "Central African Republic": qex="car"
				elif quizans["name"] == "Porto-Novo": qex="pn"
				elif quizans["name"] == "Guinea-Bissau": qex="gb"
				elif quizans["name"] == "Timor-Leste": qex="tl"
				else: qex=nnfixed
			qqqq = unidecode.unidecode(quizans[t])
			def check(message : discord.Message) -> bool: 
				return message.channel == channel and message.author != self.bot and (message.content.lower() == qqqq.lower() or message.content.lower() == qex)
			try:
				message = await self.bot.wait_for('message', timeout = 12.5, check = check)
			except asyncio.TimeoutError: 
				if t == "capital": 
					await em.edit(embed=discord.Embed(title="No one answered correctly!",description=f'What is the capital of `{quizans["name"]}:` \nReal Answer: `{quizans["capital"]}`',color=0xfa8e23, timestamp = datetime.utcnow()))
				else:
					await em.edit(embed=discord.Embed(title="No one answered correctly!",description=f'Which country does this flag belong to?: \nReal Answer: `{quizans["name"]}`',color=0xfa8e23, timestamp = datetime.utcnow()).set_thumbnail(url=quizans["flags"]))

			else: 
				with open('lb.json', 'r+') as f:
					data = json.load(f)
				if str(message.author.id) not in amounts.keys():
					amounts[str(message.author.id)] = 1
					_save()
				else:
					amounts[str(message.author.id)] += 1
					_save()
				totals=amounts[str(message.author.id)]
				if totals==1000:
					await message.author.send("""
					```ansi
					You are officially a [1;33m[1;40mnerd![0m You gain the [1;34m[1;40m@Oceanographer role[0m, and access to the the [1;32m[1;40mGeography Nerds[0m special chat which gives you access to on demand games of quizes.
					[1;4;37m[1;41m(Please do not leak the Special chat if you do you will get removed, and your score will be wiped!)
					```""")
					await message.author.add_roles(role=guild.get_role(954556452087922730))
					await self.bot.get_channel(808448077614415882).send(f"New <@&954556452087922730>! \nGGs to {message.author.mention} for getting 1000 countries/flags correct!")
				await message.add_reaction("✅")
				if t == "capital": await em.edit(embed=discord.Embed(title=f'{message.author} answered correctly!',description=f'What is the capital of `{quizans["name"]}`: \nAnswer: `{quizans["capital"]}`', color=0x3cb556, timestamp = datetime.utcnow()).set_author(name=message.author,icon_url=message.author.avatar_url).set_footer(text=f"They have a total of {totals} point(s)!"))
				else: await em.edit(embed=discord.Embed(title=f'{message.author} answered correctly!',description=f'Which country does this flag belong to? \nAnswer: `{quizans["name"]}`', color=0x3cb556, timestamp = datetime.utcnow()).set_thumbnail(url=quizans["flags"]).set_author(name=message.author,icon_url=message.author.avatar_url).set_footer(text=f"They have a total of {totals} point(s)!"))
			finally: 
				print("Done")

	@countries.before_loop
	async def before_countries(self):
		print('Starting')
		await self.bot.wait_until_ready()

def _save():
    with open('lb.json', 'w+') as f:
        json.dump(amounts, f)
def setup(bot):
	bot.add_cog(Countries(bot))
