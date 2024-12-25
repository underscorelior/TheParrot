import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

DB_URL = os.getenv("NEON_URL")

class Reload(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["wl"])
    async def whitelist(self, ctx: commands.Context[commands.Bot], id: int):
        if ctx.author.id == self.bot.owner_id:
            conn = psycopg2.connect(DB_URL)
            cur = conn.cursor()

            cur.execute(f"INSERT INTO whitelist (users) VALUES ({id})")
            cur.execute(f"SELECT users FROM whitelist")

            await ctx.send(f"**Whitelisted {id}**\nCurrent WL: {list(map(lambda x: int(x[0]), cur.fetchall()))}")
            
            
            cur.close()
            conn.commit()
            conn.close()
            
    @commands.command(aliases=["rl"])
    async def reload(self, ctx: commands.Context[commands.Bot]):
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        cur.execute(f"SELECT users FROM whitelist")        
        wl = cur.fetchall() 
        cur.close()
        conn.commit()
        conn.close()
        
        wl = list(map(lambda x: int(x[0]), wl))
        
        if ctx.author.id in wl or ctx.author.id == self.bot.owner_id:
            await discord.utils.maybe_coroutine(self.bot.reload_extension, 'cogs.countries')
            await ctx.reply("🔁 `cogs.countries`", mention_author=False)
        else: 
            await ctx.reply("You do not have the required permission to reload!", delete_after=2.5)


async def setup(bot):
    await bot.add_cog(Reload(bot))
