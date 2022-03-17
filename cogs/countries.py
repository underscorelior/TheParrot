from discord.ext import tasks, commands
from discord.utils import get
import random
import aiohttp
import discord
from datetime import datetime
import asyncio
import time
	
class Countries(commands.Cog):
	def __init__(self, bot):
		self.index = 0
		self.bot = bot
		self.countries.start()

	def cog_unload(self):
		self.countries.cancel()
	#after winner, add message for til next round
	@tasks.loop(seconds=35)
	async def countries(self):
		t = random.randint(1,2)
		guild=self.bot.get_guild(722086066596741144)
		channel = get(guild.text_channels, topic=str("Country quiz, new game starts every 35 seconds!"))
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
			message = await self.bot.wait_for('message', timeout = 30.5, check = check)
		except asyncio.TimeoutError: 
			if t == "capital": 
				await em.edit(embed=discord.Embed(title="No one answered correctly!",description=f'What is the capital of `{quizans["name"]}:` \nReal Answer: `{quizans["capital"]}`',color=0xfa8e23, timestamp = datetime.utcnow()))
			else:
				await em.edit(embed=discord.Embed(title="No one answered correctly!",description=f'Which country does this flag belong to?: \nReal Answer: `{quizans["name"]}`',color=0xfa8e23, timestamp = datetime.utcnow()).set_thumbnail(url=quizans["flags"]))
		else: 
			if t == "capital": await em.edit(embed=discord.Embed(title=f'{message.author} answered correctly!',description=f'What is the capital of `{quizans["name"]}`: \nAnswer: `{quizans["capital"]}`', color=0x3cb556, timestamp = datetime.utcnow()).set_author(name=message.author,icon_url=message.author.avatar_url))
			else: await em.edit(embed=discord.Embed(title=f'{message.author} answered correctly!',description=f'Which country does this flag belong to? \nAnswer: `{quizans["name"]}`', color=0x3cb556, timestamp = datetime.utcnow()).set_thumbnail(url=quizans["flags"]).set_author(name=message.author,icon_url=message.author.avatar_url))
			await message.add_reaction("✅")
		finally: 
			print("Done")
	@countries.before_loop
	async def before_countries(self):
		print('Starting')
		await self.bot.wait_until_ready()


def setup(bot):
	bot.add_cog(Countries(bot))