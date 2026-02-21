import discord
from discord.ext import commands
import aiohttp
import asyncio
import os

class user(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sites = [
            'https://youtube.com/@', 'https://www.linkedin.com/in/', 'https://github.com/',
            'https://www.snapchat.com/add/', 'https://www.tumblr.com/', 'https://www.vk.com/',
            'https://www.flickr.com/photos/', 'https://www.behance.net/', 'https://www.deviantart.com/',
            'https://www.quora.com/profile/', 'https://www.vimeo.com/', 'https://www.foursquare.com/',
            'https://www.mix.com/', 'https://www.wattpad.com/user/', 'https://www.replit.com/@',
            'https://www.gitlab.com/', 'https://www.stackoverflow.com/users/', 'https://www.codepen.io/',
            'https://www.podbean.com/', 'https://www.tripadvisor.com/members/', 'https://www.yelp.com/user_details/',
            'https://www.scribd.com/user/', 'https://www.strava.com/athletes/', 'https://www.imdb.com/user/',
            'https://www.amazon.com/', 'https://www.fiverr.com/', 'https://www.upwork.com/',
            'https://www.blogger.com/', 'https://www.etsy.com/shop/', 'https://www.deezer.com/',
            'https://www.soundcloud.com/', 'https://www.livejournal.com/', 'https://www.airbnb.com/users/',
            'https://www.makerbot.com/profiles/', 'https://www.xbox.com/en-US/profile/'
        ]

    async def check_site(self, session, url, username):
        target = f"{url}{username}"
        try:
            async with session.get(target, timeout=5) as response:
                if response.status == 200:
                    return target
        except:
            return None
        return None

    @commands.command()
    async def user(self, ctx, username: str):

        async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
            tasks = [self.check_site(session, site, username) for site in self.sites]
            results = await asyncio.gather(*tasks)

        found_sites = [res for res in results if res]
        
        if found_sites:
            result_text = "\n".join(found_sites)
        else:
            result_text = "No profiles found."

        embed = discord.Embed(
            title=f"🔎 Spartan Results For {username}", 
            description=f"```{result_text}```", 
            color=0x2e2e2e
        )
        embed.set_footer(text="Spartan | OSINT Intelligence")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(user(bot))