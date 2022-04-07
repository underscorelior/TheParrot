from discord.ext import tasks, commands
from utils import winbtn, losebtn, checkans, toembed, toembedt
from discord.utils import get
import random
import aiohttp
import discord
from datetime import datetime
import asyncio
import json
from unidecode import unidecode
from discord_components import Button, ButtonStyle
from re import sub
global amounts
try:
	print("Successfully loaded amounts.json")
	with open('quizlb.json') as f:
		amounts = json.load(f)
except FileNotFoundError:
	print("Could not load amounts.json")

	
def _parse_(content: str) -> str:
	return sub(r"[\d\?\!.,/\']","",unidecode(content).strip().lower()).replace("-", " ")
	
class Countries(commands.Cog):
	def __init__(self, bot):
		self.index = 0
		self.bot = bot
		self.countries.start()
	global xpgain
	xpgain=1
	@commands.command(aliases=["lb"])
	async def leaderboard(self,ctx):
		guild=self.bot.get_guild(722086066596741144)
		channel = get(guild.text_channels, topic=str("Country quiz, new game starts every 15 seconds! https://github.com/underscorelior/TheParrot"))
		if channel.id == ctx.channel.id or ctx.channel.id == 955169257711370280:
			with open('quizlb.json', 'r') as f:
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
				async with session.get("https://komali.dev/bin/territories.json", ssl=False) as f: altdata = await f.json()
			
			quizans=data[random.randint(0,len(data)-1)]
			ccfixed = quizans["capital"]
			nnfixed = unidecode(quizans["name"])
			if t == 1 and ccfixed:
				t="capital"
				if quizans["capital"] == "City of San Marino": 	quizans["capital"]=qex="San Marino"
				else: qex=ccfixed
				msem = discord.Embed(title=f'What is the capital of `{quizans["name"]}`:',color=0x1860cc, timestamp = datetime.utcnow())
				ccfixed = unidecode(ccfixed)
			else:
				if random.randint(1,17) == 7: 
					quizans=altdata[random.randint(0,len(altdata)-1)]
					tc=1
				else:tc=2
				t = "name"
				msem = discord.Embed(title=f'Which {"country" if tc==2 else "territory"} does this flag belong to?',color=0x1860cc, timestamp = datetime.utcnow()).set_image(url=quizans["flags"])
			em = await channel.send(embed=msem)	
			qqqq = quizans[t]
			def check(message : discord.Message) -> bool: 
				content = _parse_(message.content)
				if content == "usa": content = "United States" 
				if content == "uae": content = "United Arab Emirates"
				if content == "uk": content = "United Kingdom"
				if content == "nk": content = "North Korea"
				if content == "sk": content = "South Korea"
				if content == "nz": content =  "New Zealand"
				if content == "roc": content =  "Republic of the Congo"
				if content == "drc": content =  "DR Congo"
				if content == "dr": content =  "Dominican Republic"
				if content == "svg": content =  "Saint Vincent and the Grenadines"
				if content == "png": content =  "Papua New Guinea"
				if content == "ab": content =  "Antigua and Barbuda"
				if content == "sa": content =  "Saudi Arabia"
				if content == "sl": content =  "Sierra Leone"
				if content == "tt": content =  "Trinidad and Tobago"
				if content == "bh": content =  "Bosnia and Herzegovina"
				if content == "skn": content =  "Saint Kitts and Nevis"
				if content == "stp": content =  "São Tomé and Príncipe"
				if content == "car": content =  "Central African Republic"
				if content == "gb": content =  "Guinea-Bissau"
				if content == "tl": content =  "Timor-Leste"
				if content == "nc": content =  "New Caledonia"
				if content == "spm": content =  "Saint Pierre and Miquelon"
				if content == "biot": content =  "British Indian Ocean Territory"
				if content == "cki": content =  "Cocos (Keeling) Islands"
				if content == "nmi": content =  "Northern Mariana Islands"
				if content == "tci": content = "Turks and Caicos Islands"
					
				# Capitals
				if content == "dc": content =  "Washington, D.C."
				
				return message.channel == channel and message.author != self.bot and (content == _parse_(qqqq))
			try:
				message = await self.bot.wait_for('message', timeout = 12.5, check = check)
			except asyncio.TimeoutError: 
				if t == "capital":
					await em.edit(embed=discord.Embed(title="No one answered correctly!",description=f'What is the capital of `{quizans["name"]}:` \nReal Answer: `{quizans["capital"]}`',color=0xfa8e23, timestamp = datetime.utcnow()))
				else:
					await em.edit(embed=discord.Embed(title="No one answered correctly!",description=f'Which {"country" if tc==2 else "territory"} does this flag belong to?: \nReal Answer: `{quizans["name"]}`',color=0xfa8e23, timestamp = datetime.utcnow()).set_thumbnail(url=quizans["flags"]))

			else: 
				with open('quizlb.json', 'r+') as f:
					data = json.load(f)
				if str(message.author.id) not in amounts.keys():
					amounts[str(message.author.id)] = xpgain
					_save()
				else:
					amounts[str(message.author.id)] += xpgain
					_save()
				totals=amounts[str(message.author.id)]

				if totals==1000:
					await message.author.send("""
```ansi
You are officially a [1;33m[1;40mnerd![0m You gain the [1;34m[1;40m@Oceanographer role[0m, and access to the the [1;32m[1;40mGeography Nerds[0m special chat which gives you access to on demand games of quizes.	
[1;4;37m[1;41m(Please do not leak the Special chat if you do you will get removed, and your score will be wiped!)
```""")
					role=get(guild.roles, name="Oceanographers")
					member = guild.get_member(message.author.id)
					await member.add_roles(role)
					await self.bot.get_channel(808448077614415882).send(f"New <@&954556452087922730>! \nGGs to {message.author.mention} for getting 1000 countries/flags correct!")
				await message.add_reaction("✅")
				if t == "capital": await em.edit(embed=discord.Embed(title=f'{message.author} answered correctly!',description=f'What is the capital of `{quizans["name"]}`: \nAnswer: `{quizans["capital"]}`', color=0x3cb556, timestamp = datetime.utcnow()).set_author(name=message.author,icon_url=message.author.avatar_url).set_footer(text=f"They have a total of {totals} point(s)!"))
				else: await em.edit(embed=discord.Embed(title=f'{message.author} answered correctly!',description=f'Which {"country" if tc==2 else "territory"} does this flag belong to? \nAnswer: `{quizans["name"]}`', color=0x3cb556, timestamp = datetime.utcnow()).set_thumbnail(url=quizans["flags"]).set_author(name=message.author,icon_url=message.author.avatar_url).set_footer(text=f"They have a total of {totals} point(s)!"))

			finally: 
				print("Done")
	@commands.command(aliases=["q"])
	async def quiz(self,ctx):
		if ctx.channel.id == 955169257711370280:
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
				with open('quizlb.json', 'r+') as f:
					data = json.load(f)
				amounts[str(ctx.author.id)] += xpgain
				_save()
				if qtype==1:await message.edit(embed=discord.Embed(title='Win',description=f'What is the capital of `{quizans["name"]}`: \nAnswer: `{quizans["capital"]}`', color=0x3cb556, timestamp = datetime.utcnow()).set_footer(text=f'{ctx.author} | {amounts[str(ctx.author.id)]} Point(s)',icon_url=ctx.author.avatar_url),components=await winbtn(ansloc))
				else:await message.edit(embed=discord.Embed(title='Win',description=f'Which country does this flag belong to? \nAnswer: `{quizans["name"]}`', color=0x3cb556, timestamp = datetime.utcnow()).set_footer(text=f'{ctx.author} | {amounts[str(ctx.author.id)]} Point(s)',icon_url=ctx.author.avatar_url).set_thumbnail(url=quizans["flags"]),components=await winbtn(ansloc))
			else:
				qta = await losebtn(int(ansch.custom_id),ansloc)
				if qtype==1:await message.edit(embed=discord.Embed(title='Lose',description=f'What is the capital of `{quizans["name"]}`: \nSelected Answer: `{btnans[0][qta[1]-1].label}` \nReal Answer: `{quizans["capital"]}`',color=0xfa8e23, timestamp = datetime.utcnow()).set_footer(text=f'{ctx.author} | {amounts[str(ctx.author.id)]} Point(s)',icon_url=ctx.author.avatar_url),components=qta[0])
				else:await message.edit(embed=discord.Embed(title='Lose',description=f'Which country does this flag belong to? \nSelected Answer: `{btnans[0][qta[1]-1].label}` \nReal Answer: `{quizans["name"]}``', color=0xfa8e23, timestamp = datetime.utcnow()).set_footer(text=f'{ctx.author} | {amounts[str(ctx.author.id)]} Point(s)',icon_url=ctx.author.avatar_url).set_thumbnail(url=quizans["flags"]),components=await winbtn(ansloc))

	@countries.before_loop
	async def before_countries(self):
		print('Starting')
		await self.bot.wait_until_ready()

def _save():
    with open('quizlb.json', 'w+') as f:
        json.dump(amounts, f)
def setup(bot):
	bot.add_cog(Countries(bot))
