from utils import winbtn, losebtn, checkans, toembed, toembedt
import discord
import random
import aiohttp
from datetime import datetime
import asyncio
import json
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord_components import Button, ButtonStyle
try:
	print("Successfully loaded lb.json")
	with open('lb.json') as f:
		amounts = json.load(f)
except FileNotFoundError:
	print("Could not load lb.json")

class CountryQuiz(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot
	@commands.command(aliases=["q"])
	async def quiz(self,ctx):
		if ctx.channel.id == 954989125696618496:
			async with aiohttp.ClientSession() as session: 
				async with session.get("https://underscore.wtf/countries/countries.json", ssl=False) as r: data = await r.json()
			quizans=data[random.randint(0,len(data)-1)]
			ansloc = random.randint(1,4) 
			qtype=random.randint(1,2)
			if qtype==1:qt="capital"
			else:qt="name"
			ca=await checkans(data, ansloc, quizans, qt)
			btnans=[[Button(label=ca[0], emoji="🇦", style=ButtonStyle.blue, custom_id=1),Button(label=ca[1],emoji='🇧', style=ButtonStyle.blue, custom_id=2),Button(label=ca[2], emoji="🇨", style=ButtonStyle.blue, custom_id=3),Button(label=ca[3], emoji='🇩', style=ButtonStyle.blue, custom_id=4)]]
			if qtype==1:msem = discord.Embed(title=f'What is the capital of `{quizans["name"]}`:',color=0x1860cc, timestamp = datetime.utcnow()).set_footer(text=ctx.author,icon_url=ctx.author.avatar_url)
			else:msem = discord.Embed(title=f'Which country does this flag belong to?',color=0x1860cc, timestamp = datetime.utcnow()).set_image(url=quizans["flags"]).set_footer(text=ctx.author,icon_url=ctx.author.avatar_url)
			message = await ctx.send(content=ctx.author.mention,embed=msem,components=btnans)
			try: 
				ansch = await self.bot.wait_for('button_click',check=lambda inter: inter.message.id == message.id and inter.user.id == ctx.author.id,timeout=15)
			except asyncio.TimeoutError: 
				if qtype==1:return await message.edit(embed=await toembed(f'What is the capital of `{quizans["name"]}`: \nAnswer: `{quizans["capital"]}`'),components=[[Button(emoji="🇦",style=ButtonStyle.grey,disabled=True),Button(emoji='🇧',style=ButtonStyle.grey,disabled=True),Button(emoji="🇨",style=ButtonStyle.grey,disabled=True),Button(emoji='🇩',style=ButtonStyle.grey,disabled=True)]])
				else:return await message.edit(embed=await toembedt(f'Which country does this flag belong to? \nAnswer: `{quizans["name"]}`',quizans["flags"]),components=[[Button(emoji="🇦",style=ButtonStyle.grey,disabled=True),Button(emoji='🇧',style=ButtonStyle.grey,disabled=True),Button(emoji="🇨",style=ButtonStyle.grey,disabled=True),Button(emoji='🇩',style=ButtonStyle.grey,disabled=True)]])
			if int(ansch.custom_id) == ansloc:
				with open('lb.json', 'r+') as f:
					data = json.load(f)
					if str(ctx.author.id) not in amounts.keys():
						amounts[str(ctx.author.id)] = 1
						_save()
					else:
						amounts[str(ctx.author.id)] += 1
						_save()
				if qtype==1:await message.edit(embed=discord.Embed(title='Win',description=f'What is the capital of `{quizans["name"]}`: \nAnswer: `{quizans["capital"]}`', color=0x3cb556, timestamp = datetime.utcnow()).set_footer(text=f'{ctx.author} | {amounts[str(ctx.author.id)]} Point(s)',icon_url=ctx.author.avatar_url),components=await winbtn(ansloc))
				else:await message.edit(embed=discord.Embed(title='Win',description=f'Which country does this flag belong to? \nAnswer: `{quizans["name"]}`', color=0x3cb556, timestamp = datetime.utcnow()).set_footer(text=f'{ctx.author} | {amounts[str(ctx.author.id)]} Point(s)',icon_url=ctx.author.avatar_url).set_thumbnail(url=quizans["flag"]),components=await winbtn(ansloc))
			else:
				qta = await losebtn(int(ansch.custom_id),ansloc)
				if qtype==1:await message.edit(embed=discord.Embed(title='Lose',description=f'What is the capital of `{quizans["name"]}`: \nSelected Answer: `{btnans[0][qta[1]-1].label}` \nReal Answer: `{quizans["capital"]}`',color=0xfa8e23, timestamp = datetime.utcnow()).set_footer(text=f'{ctx.author} | {amounts[str(ctx.author.id)]} Point(s)',icon_url=ctx.author.avatar_url),components=qta[0])
				else:await message.edit(embed=discord.Embed(title='Lose',description=f'Which country does this flag belong to? \nSelected Answer: `{btnans[0][qta[1]-1].label}` \nReal Answer: `{quizans["name"]}``', color=0xfa8e23, timestamp = datetime.utcnow()).set_footer(text=f'{ctx.author} | {amounts[str(ctx.author.id)]} Point(s)',icon_url=ctx.author.avatar_url).set_thumbnail(url=quizans["flag"]),components=await winbtn(ansloc))

def _save():
    with open('lb.json', 'w+') as f:
        json.dump(amounts, f)
def setup(bot: commands.Bot):
	bot.add_cog(CountryQuiz(bot))
