import discord
from discord.ext import commands
import aiohttp
import json
import os

class breach(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def breach(self, ctx, email: str):
        url = f"https://api.xposedornot.com/v1/check-email/{email}"
        filename = f"breach_{ctx.author.id}.json"
        
        async with aiohttp.ClientSession() as session:
            
            try:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        breach_list = data.get("breaches", [])
                        
                        result_text = "\n".join([f"• {b[0]}" for b in breach_list[:10]])
                        if len(breach_list) > 10:
                            result_text += f"\n...and {len(breach_list) - 10} more."

                        with open(filename, "w") as f:
                            json.dump(data, f, indent=4)

                        embed = discord.Embed(
                            title=f"🔎 Spartan Results For {email}", 
                            color=0x2e2e2e
                        )
                        embed.add_field(name="📂 Breaches Found", value=f"```{len(breach_list)}```", inline=True)
                        embed.add_field(name="📝 Breach List", value=f"```{result_text if result_text else 'None'}```", inline=False)
                        
                        embed.set_footer(text="Spartan | OSINT Intelligence")
                        
                        await ctx.send(embed=embed, file=discord.File(filename))
                    
                    elif response.status == 404:
                        embed = discord.Embed(title=f"🔎 Spartan Results For {email}", color=0x2e2e2e)
                        embed.add_field(name="🛡️ Status", value="```Secure / No Breaches Found```", inline=False)
                        embed.set_footer(text="Spartan | OSINT Intelligence")
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f"API Error: {response.status}")
            
            except Exception as e:
                await ctx.send(f"Error: `{str(e)}`")
            
            finally:
                if os.path.exists(filename):
                    os.remove(filename)

async def setup(bot):
    await bot.add_cog(breach(bot))