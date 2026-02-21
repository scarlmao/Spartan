import discord
from discord.ext import commands
import requests
import json
import os

class court(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

    def get_api_token(self):
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f).get("courtlistener_api")
        except:
            return None

    @commands.command(name="court")
    async def court(self, ctx, *, casen: str):
        api_token = self.get_api_token()
        if not api_token:
            return await ctx.send("CourtListener API token not found in config.")

        url = f'https://www.courtlistener.com/api/rest/v4/search/?q={casen}'
        headers = {'Authorization': f'Token {api_token}'}
        filename = f"cases_{ctx.author.id}.json"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                cases_info = []
                
                for case in data.get('results', []):
                    case_info = {
                        'caseName': case.get('caseName', 'N/A'),
                        'court': case.get('court', 'N/A'),
                        'dateFiled': case.get('dateFiled', 'N/A'),
                        'docketNumber': case.get('docketNumber', 'N/A'),
                        'judge': case.get('judge', 'N/A'),
                        'status': case.get('status', 'N/A'),
                        'url': f"https://www.courtlistener.com{case.get('absolute_url', '')}",
                        'opinion_url': case['opinions'][0].get('download_url', 'N/A') if case.get('opinions') else 'N/A',
                        'snippet': case['opinions'][0].get('snippet', 'N/A') if case.get('opinions') else 'N/A'
                    }
                    cases_info.append(case_info)

                if not cases_info:
                    return await ctx.send(f"No results found for `{casen}`.")

                with open(filename, "w") as file:
                    json.dump(cases_info, file, indent=2)

                embed = discord.Embed(
                    title=f"🔎 Spartan Results For {casen}", 
                    description=f"Found {len(cases_info)} record(s). Detailed data attached.",
                    color=0x2e2e2e
                )
                embed.set_footer(text="Spartan | OSINT Intelligence")

                await ctx.send(embed=embed, file=discord.File(filename))
            else:
                await ctx.send(f"failed with status code {response.status_code}")

        except Exception as e:
            await ctx.send(f"Error: `{e}`")

        finally:
            if os.path.exists(filename):
                os.remove(filename)

async def setup(bot):
    await bot.add_cog(court(bot))