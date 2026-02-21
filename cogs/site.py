import discord
from discord.ext import commands
import requests
import json
import os

class site(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

    def get_auth_token(self):
        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                return data.get("host_io")
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    @commands.command()
    async def site(self, ctx, site_url: str):
        auth = self.get_auth_token()
        cleaned_site = site_url.replace("https://", "").replace("http://", "").split('/')[0]
        
        if not auth:
            return await ctx.send("API Key not found in config.json.")

        try:
            r_main = requests.get(f'https://host.io/api/web/{cleaned_site}?token={auth}', timeout=10).json()
            ip = r_main.get("ip", "N/A")
            links = r_main.get("links", "N/A")
            encoding = r_main.get("encoding", "N/A")

            r_rel = requests.get(f'https://host.io/api/related/{cleaned_site}?token={auth}', timeout=10).json()
            redirects = r_rel.get("redirects", [{}])[0].get("count", 0)
            backlinks = r_rel.get("backlinks", [{}])[0].get("count", 0)
            asn_count = r_rel.get("asn", [{}])[0].get("count", 0)

            r_geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
            country = r_geo.get('country', 'None')
            region = r_geo.get('regionName', 'None')
            city = r_geo.get('city', 'None')

        except Exception as e:
            return await ctx.send(f"Error: `{e}`")

        embed = discord.Embed(
            title="🔎 Site Results",
            description=f"Information for **{site_url}**",
            color=0x2e2e2e
        )

        embed.add_field(name="🌐 IP", value=f"```{ip}```", inline=True)
        embed.add_field(name="🔗 Links", value=f"```{links}```", inline=True)
        embed.add_field(name="📄 Encoding", value=f"```{encoding}```", inline=True)
        embed.add_field(name="🔀 Redirects", value=f"```{redirects}```", inline=True)
        embed.add_field(name="🔙 Backlinks", value=f"```{backlinks}```", inline=True)
        embed.add_field(name="📡 ASN Count", value=f"```{asn_count}```", inline=True)
        embed.add_field(name="🌍 Country", value=f"```{country}```", inline=True)
        embed.add_field(name="📍 Region", value=f"```{region}```", inline=True)
        embed.add_field(name="🏙️ City", value=f"```{city}```", inline=True)

        embed.set_footer(text="Spartan | OSINT Intelligence")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(site(bot))