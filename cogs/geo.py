import discord
from discord.ext import commands
import os
import json
from picarta import Picarta

class geo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

    def get_api_token(self):
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f).get("picarta_api")
        except:
            return None

    @commands.command()
    async def geo(self, ctx):
        if len(ctx.message.attachments) == 0:
            return await ctx.send("Please attach an image to localize.")

        api_token = self.get_api_token()
        if not api_token:
            return await ctx.send("Picarta API token not found in config.")

        attachment = ctx.message.attachments[0]
        image_path = f"temp_{attachment.filename}"
        
        try:
            await attachment.save(image_path)

            localizer = Picarta(api_token)
            result = localizer.localize(img_path=image_path)

            confidence = result.get("ai_confidence", "N/A")
            province = result.get("province", "N/A")
            country = result.get("ai_country", "N/A")
            city = result.get("city", "N/A")

            embed = discord.Embed(title="🔎 Spartan Geo Results", color=0x2e2e2e)
            embed.add_field(name="👁️ Confidence", value=f"```{confidence}```", inline=True)
            embed.add_field(name="🌍 Country", value=f"```{country}```", inline=False)
            embed.add_field(name="📍 State/Province", value=f"```{province}```", inline=False)
            embed.add_field(name="🌆 City", value=f"```{city}```", inline=False)
            embed.set_footer(text="Spartan | OSINT Intelligence")
            
            await ctx.send(embed=embed)

        finally:
            if os.path.exists(image_path):
                os.remove(image_path)

async def setup(bot):
    await bot.add_cog(geo(bot))