import discord
from discord.ext import commands
import requests
import json
import os

class virustotal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

    def get_api_key(self):
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f).get("virustotal_api")
        except:
            return None

    @commands.command()
    async def virustotal(self, ctx, hash_value: str):
        api_key = self.get_api_key()
        if not api_key:
            return await ctx.send("VirusTotal API key not found in config.")

        url = f'https://www.virustotal.com/api/v3/files/{hash_value}'
        headers = {'x-apikey': api_key}
        filename = f"{hash_value}.json"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                stats = data['data']['attributes']['last_analysis_stats']
                malicious = stats.get('malicious', 0)
                
                result = {
                    'hash': hash_value,
                    'malicious_detections': malicious,
                    'stats': stats,
                    'full_report': data
                }

                with open(filename, 'w') as file:
                    json.dump(result, file, indent=4)

                embed = discord.Embed(title=f"🔎 Spartan VIrusTotal Results", color=0x2e2e2e)
                embed.add_field(name="🧬 Hash", value=f"```{hash_value}```", inline=False)
                embed.add_field(name="🚩 Detections", value=f"```{malicious} Engines```", inline=True)
                embed.set_footer(text="Spartan | OSINT Intelligence")

                await ctx.send(embed=embed, file=discord.File(filename))
            
            elif response.status_code == 404:
                await ctx.send(f"Hash `{hash_value}` not found in VirusTotal database.")
            else:
                await ctx.send(f"Error: API returned status code {response.status_code}")

        except Exception as e:
            await ctx.send(f"Error: `{e}`")
            
        finally:
            if os.path.exists(filename):
                os.remove(filename)

async def setup(bot):
    await bot.add_cog(virustotal(bot))