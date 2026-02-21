import discord
from discord.ext import commands
import requests
import os

class dlookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scammer_url = "https://raw.githubusercontent.com/im-silent/newdbs/refs/heads/main/dbs/ScammerAlert!%20-%20ALERTS%20-%20%E2%9B%94%E2%94%83known-scammers%20%5B888763420055318559%5D.csv"
        self.restorecord_url = "https://raw.githubusercontent.com/im-silent/newdbs/refs/heads/main/dbs/RestoreCord.sql"

    def find_line_in_db(self, url, uid):
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                lines = r.text.splitlines()
                for line in lines:
                    if uid in line:
                        return line
            return None
        except:
            return None

    @commands.command()
    async def dlookup(self, ctx, uid: str):
        try:
            user = await self.bot.fetch_user(int(uid))
            username = f"{user.name}#{user.discriminator}" if user.discriminator != "0" else user.name
        except:
            username = "Not Found"

        scammer_line = self.find_line_in_db(self.scammer_url, uid)
        is_scammer = "True" if scammer_line else "False"
        
        restorecord_line = self.find_line_in_db(self.restorecord_url, uid)
        leak_display = restorecord_line if restorecord_line else "None Found"

        embed = discord.Embed(
            title=f"🔎 Spartan Results For {uid}", 
            color=0x2e2e2e
        )
        
        embed.add_field(name="🌐 User ID", value=f"```{uid}```", inline=False)
        embed.add_field(name="👤 Username", value=f"```{username}```", inline=True)
        embed.add_field(name="🚫 Scammer Status", value=f"```{is_scammer}```", inline=True)
        embed.add_field(name="📂 Leaked Info", value=f"```{leak_display}```", inline=False)
        
        embed.set_footer(text="Spartan | Osint Intelligence")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(dlookup(bot))