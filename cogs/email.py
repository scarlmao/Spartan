import discord
from discord.ext import commands
import aiohttp
import asyncio
import json
import os
import hashlib

class EmailLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

    def get_hunter_key(self):
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f).get("hunter_api", "")
        except:
            return ""

    async def fetch_status(self, session, url, method="GET", **kwargs):
        try:
            async with session.request(method, url, timeout=5, **kwargs) as r:
                return r.status, await r.text()
        except:
            return 500, ""

    @commands.command()
    async def email(self, ctx, email: str):
        hunter_key = self.get_hunter_key()
        output_file = f"result_{ctx.author.id}.json"
        
        async with aiohttp.ClientSession() as session:
            

            
            email_hash = hashlib.md5(email.encode()).hexdigest()
            
            
            tasks = [
                session.get(f"https://api.github.com/search/users?q={email}+in:email"),
                session.post("https://www.chess.com/callback/email/available", data={'email': email}),
                session.get(f"https://www.gravatar.com/{email_hash}.json"),
                session.post('https://api.accounts.firefox.com/v1/account/status', json={"email": email}),
                session.get(f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-email?email={email}"),
                session.get(f"https://leakcheck.net/api/public?key=49535f49545f5245414c4c595f4150495f4b4559&check={email}")
            ]

            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
          
            data = {
                "target": email,
                "social_media": {},
                "breaches": [],
                "stealer_logs": {}
            }
            for i, res in enumerate(responses):
                if isinstance(res, Exception) or res is None: continue
                
                try:
                    js = await res.json()
                    if i == 0: 
                        data["social_media"]["GitHub"] = js.get("items", [{}])[0].get("login") if js.get("total_count") else "None"
                    elif i == 1: 
                        data["social_media"]["Chess"] = "Found" if not js.get("isEmailAvailable") else "None"
                    elif i == 2: 
                        data["social_media"]["Gravatar"] = js.get("entry", [{}])[0].get("preferredUsername") if "entry" in js else "None"
                    elif i == 3: 
                        data["social_media"]["Firefox"] = "Found" if "true" in await res.text() else "None"
                    elif i == 4: 
                        if js.get("stealers"):
                            data["stealer_logs"] = js["stealers"][0]
                    elif i == 5: 
                        if "sources" in js:
                            data["breaches"] = [f"{s['name']} ({s['date']})" for s in js["sources"]]
                except:
                    continue

            
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=4)

            try:
                embed=discord.Embed(title=f"Spartan Results For {email}", color=0x2e2e2e)
                embed.set_footer(text="Spartan | Osint Intelligence")
                await ctx.send(embed=embed, file=discord.File(output_file))
            finally:
                
                if os.path.exists(output_file):
                    os.remove(output_file)

async def setup(bot):
    await bot.add_cog(EmailLookup(bot))