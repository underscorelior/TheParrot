import discord,os,time
from discord.utils import get
from discord.ext import commands
from discord_components import DiscordComponents
from utils import userembed ,waitembed,infoembed, modembed
from dotenv import load_dotenv
bot = commands.Bot(command_prefix=['p-', 'P-'],intents=discord.Intents.all())
@bot.event
async def on_ready():print(f"Logged in as {bot.user.name} at {time.ctime()}");await bot.change_presence(status=discord.Status.idle,activity=discord.Activity(type=discord.ActivityType.watching, name="The Bread Pirate eating crackers."));DiscordComponents(bot)
@bot.event
async def on_message(message):
	await bot.process_commands(message); ctx,guild,user=await bot.get_context(message),bot.get_guild(722086066596741144),message.author
	if not isinstance(message.channel, discord.DMChannel) or message.author.id == bot.user.id:
		if ctx.channel.category_id == 809144803749134357: 
			userid=int(ctx.channel.topic);mod=message.author;dmuser = bot.get_user(userid)
			if message.content.startswith('-r') and mod.id != 808400358317490236: msg = str(message.content).replace("-r",""); await modembed(ctx,dmuser,msg,message)
	else:
		channelname,cate,channel=str(ctx.author).replace("#","-").replace(" ","-").lower(),bot.get_channel(809144803749134357),get(guild.text_channels, topic=str(message.author.id))
		if not channel: channel = await guild.create_text_channel(name=channelname,category=cate,topic=message.author.id); await infoembed(message,channel,guild); await waitembed(user,message); await userembed(user, message,channel)
		else: await userembed(user, message,channel)
bot.load_extension("cogs.moderation");bot.load_extension("cogs.reports")
load_dotenv()
token = os.environ.get("TOKEN")
bot.run(token)