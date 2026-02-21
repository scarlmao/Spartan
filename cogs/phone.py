import discord
from discord.ext import commands
import requests


class phone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def phone(self, ctx, phone_number: str):
        try:
            response = requests.get(
                f"https://api.numlookupapi.com/v1/validate/{phone_number}",
                timeout=10
            )
            data = response.json()
        except Exception:
            return await ctx.send("API failed.")

        if not data.get("valid"):
            return await ctx.send("Invalid phone number.")

        country = data.get("country_name", "None")
        country_code = data.get("country_code", "None")
        location = data.get("location", "None")
        carrier = data.get("carrier", "None")
        line_type = data.get("line_type", "None")

        embed = discord.Embed(
            title="🔎 Phone Results",
            color=0x2e2e2e
        )

        embed.add_field(name="📞 Phone Number", value=f"```{phone_number}```", inline=True)
        embed.add_field(name="🌍 Country", value=f"```{country}```", inline=True)
        embed.add_field(name="🔢 Country Code", value=f"```{country_code}```", inline=True)
        embed.add_field(name="📫 Location", value=f"```{location}```", inline=True)
        embed.add_field(name="📡 Carrier", value=f"```{carrier}```", inline=True)
        embed.add_field(name="💊 Line Type", value=f"```{line_type}```", inline=True)

        embed.set_footer(text="Spartan | OSINT Intelligence")

        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(phone(bot))