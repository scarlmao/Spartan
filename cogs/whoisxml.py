import discord
from discord.ext import commands
import requests
import json
import os

class whoisxml(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

    def get_api_key(self):
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f).get("whoisxml_api")
        except:
            return None

    @commands.command(name="whoisxml")
    async def whois_lookup(self, ctx, site: str):
        api_key = self.get_api_key()
        if not api_key:
            return await ctx.send("WhoisXML API key not found in config.")

        target = site.replace("https://", "").replace("http://", "").split('/')[0]
        filename = f"whois_{target}.json"
        
        try:
            url = f'https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={api_key}&domainName={target}&outputFormat=JSON'
            r = requests.get(url, timeout=10)
            
            if r.status_code != 200:
                return await ctx.send(f"API Error: Received status code {r.status_code}")

            with open(filename, "w") as file:
                file.write(r.text)

            embed = discord.Embed(
                title=f"🔎 Spartan Results For {target}", 
                description="Detailed WHOIS registration data attached below.",
                color=0x2e2e2e
            )
            embed.set_footer(text="Spartan | OSINT Intelligence")
            
            await ctx.send(embed=embed, file=discord.File(filename))

        except Exception as e:
            await ctx.send(f"Error: `{e}`")
            
        finally:
            if os.path.exists(filename):
                os.remove(filename)

async def setup(bot):
    await bot.add_cog(whoisxml(bot))