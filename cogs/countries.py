from discord.ext import tasks, commands
from discord.utils import get
import random
import aiohttp
import discord
from datetime import datetime
import asyncio
import json
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
	
	@commands.command()
	async def leaderboard(self,ctx):
		guild=self.bot.get_guild(722086066596741144)
		channel = get(guild.text_channels, topic=str("Country quiz, new game starts every 15 seconds! https://github.com/underscorelior/TheParrot"))
		if channel.id == ctx.channel.id:
			with open('lb.json', 'r') as f:
				data = json.load(f)
			top_users = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}
			names = ''
			for postion, user in enumerate(top_users):
				names += f'{postion+1} - <@!{user}> with {top_users[user]}\n'
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
			if message.author.id == 808400358317490236:
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
			quizans=data[random.randint(0,len(data))]
			if not quizans: quizans=data[random.randint(0,len(data))]
			if t == 1:
				msem = discord.Embed(title=f'What is the capital of `{quizans["name"]}`:',color=0x1860cc, timestamp = datetime.utcnow())
			else:
				msem = discord.Embed(title=f'Which country does this flag belong to?',color=0x1860cc, timestamp = datetime.utcnow()).set_image(url=quizans["flags"])
			em = await channel.send(embed=msem)	
			if t == 1: t="capital"
			else: t="name"
			def check(message : discord.Message) -> bool: 
				return message.channel == channel and message.author != self.bot and message.content.lower() == quizans[t].lower()
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
				await message.add_reaction("✅")
				if t == "capital": await em.edit(embed=discord.Embed(title=f'{message.author} answered correctly!',description=f'What is the capital of `{quizans["name"]}`: \nAnswer: `{quizans["capital"]}`', color=0x3cb556, timestamp = datetime.utcnow()).set_author(name=message.author,icon_url=message.author.avatar_url).set_footer(text=f"They have a total of {data[str(message.author.id)]+1} point(s)!"))
				else: await em.edit(embed=discord.Embed(title=f'{message.author} answered correctly!',description=f'Which country does this flag belong to? \nAnswer: `{quizans["name"]}`', color=0x3cb556, timestamp = datetime.utcnow()).set_thumbnail(url=quizans["flags"]).set_author(name=message.author,icon_url=message.author.avatar_url).set_footer(text=f"They have a total of {data[str(message.author.id)]+1} point(s)!"))
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