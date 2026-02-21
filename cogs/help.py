import discord
from discord.ext import commands


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
                    embed = discord.Embed(title="Spartan Commands", color=0x2e2e2e)
                    embed.add_field(name="`🌍` ip", value=f"```!ip <ip> | gives info on the ip```", inline=True)
                    embed.add_field(name="`📞` Phone", value=f"```!phone <number> | gives info on the phone number```", inline=True)
                    embed.add_field(name="`🎮` Discord", value=f"```!dlookup <id> | gives discord user info```", inline=True)
                    embed.add_field(name="`🌐` site", value=f"```!site <site> | gives info about a targeted site```", inline=True)
                    embed.add_field(name="`📫` email", value=f"```!email <email> | displays info about the email```", inline=True)  
                    embed.add_field(name="`🖼️` geo", value=f"```!geo <image> | finds location of image```", inline=True) 
                    embed.add_field(name="`❓` whoisxml", value=f"```!whoisxml <site> | finds whois xml data about a website and returns in a file```", inline=True)
                    embed.add_field(name="`👤` Username", value=f"```!user <username> | finds sites the username is signed up on```", inline=True)
                    embed.add_field(name="`📃` Osintdog", value=f"```!osintdog <query> | Looks in popular databases for a query```", inline=True)
                    embed.add_field(name="`⚖️` Court", value=f"```!court <caseName> | Info of a court case.```", inline=True)
                    embed.add_field(name="`🦠` Virus", value=f"```!virustotal <hash> | Info about program's hash.```", inline=True)
                    embed.add_field(name="`⛑️` help", value=f"```!help | sends this```", inline=True) 
                    await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(help(bot))