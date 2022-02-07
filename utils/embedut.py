import discord; from datetime import datetime; from discord.errors import HTTPException
async def infoembed(message,channel, guild): 
	user,urol=guild.get_member(message.author.id),""
	if str(user.color) == "#000000": clr = 0x1AFFCF
	else: clr = int(hex(int((str(user.color)).replace("#", ""), 16)), 0)
	if not user.nick: unick = f"{user.name} (No nick set)"
	if user.nick: unick = user.nick
	if user.roles is not None: 
		for role in user.roles[1:]: urol = role.mention + " " + urol
	else: urol = "None"
	uinfemb = discord.Embed(title=f"{user.name}", description=f"ID: {user.id}", color=clr, timestamp = datetime.utcnow()).set_thumbnail(url=user.avatar_url).set_footer(text = user.id).add_field(name="General", value=f"Nickname: {unick} \nDiscriminator: #{user.discriminator} **‖** Mention: {user.mention}").add_field(name="Server", value=f"Roles: {urol}", inline=False).add_field(name="Other", value=f"Account Created: <t:{str((user.created_at).timestamp()).split('.')[0]}:F> (<t:{str((user.created_at).timestamp()).split('.')[0]}:R>) \nJoined Server At: <t:{str((user.joined_at).timestamp()).split('.')[0]}:F> (<t:{str((user.joined_at).timestamp()).split('.')[0]}:R>)", inline=False)
	info = await channel.send(content = f"<@&914983221215772713> \n> ID: {user.id} Mention: {user.mention}",embed=uinfemb); await info.pin()
async def userembed(user, message, channel):
	try:imgs=message.attachments[0].url;embed = (discord.Embed(title=message.content, color=0x35D47A, timestamp=message.created_at).set_author(name=str(user), icon_url=user.avatar_url).set_footer(text="Id: {}".format(user.id)).set_image(url=imgs));await channel.send(embed=embed)
	except IndexError:imgs=None;embed = (discord.Embed(title=message.content, color=0x35D47A, timestamp=message.created_at).set_author(name=str(user), icon_url=user.avatar_url).set_footer(text="Id: {}".format(user.id)));await channel.send(embed=embed)
	await message.add_reaction("✅")
async def waitembed(user,message): embed=discord.Embed(title="Thank you for contacting The Parrot! Please state your inquiry if you haven't already, and a member of our moderation team will be with you shortly.",color=0xc12fed, timestamp = message.created_at).set_author(name = "The Bread Pirate's Ship",icon_url="https://cdn.discordapp.com/attachments/808448077614415882/837336840272609290/Better_bread_server.gif"); await user.send(embed=embed)
async def modembed(ctx,user,msg,message): embed=discord.Embed(title=msg,color=0x34a4eb,timestamp = message.created_at).set_author(name = "The Bread Pirate's Ship",icon_url="https://cdn.discordapp.com/attachments/808448077614415882/837336840272609290/Better_bread_server.gif"); await user.send(embed=embed); await message.delete(); await ctx.send(content=f"Sent by {message.author}",embed=embed)