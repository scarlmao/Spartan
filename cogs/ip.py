import discord
from discord.ext import commands
import requests


class ip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ip(self, ctx, ip):
        try:
            response = requests.get(
                f"http://ip-api.com/json/{ip}",
                timeout=10
            )
            data = response.json()
        except Exception:
            return await ctx.send("Failed to talk to api.")

        if data.get("status") != "success":
            return await ctx.send("Invalid IP.")


        def get(key):
            return data.get(key, "None")

        country = get("country")
        region = get("regionName")
        city = get("city")
        isp = get("isp")
        timezone = get("timezone")
        org = get("org")

        embed = discord.Embed(
            title=f"Spartan Results For {ip}",
            color=0x2e2e2e
        )

        embed.add_field(
            name="🌐 Location",
            value=f"```{country} | {region} | {city}```",
            inline=False
        )

        embed.add_field(
            name="🛜 ISP",
            value=f"```{isp}```",
            inline=False
        )

        embed.add_field(
            name="📅 Timezone",
            value=f"```{timezone}```",
            inline=False
        )

        embed.add_field(
            name="💿 Organization",
            value=f"```{org}```",
            inline=False
        )

        embed.set_footer(text="Spartan | OSINT Intelligence")

        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(ip(bot))