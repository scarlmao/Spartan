import discord
from discord.ext import commands
import json
import logging
import os
import sys
import asyncio
from pystyle import Colors, Colorate

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

token = config.get('token')
prefix = config.get('prefix')
owner = config.get('owner')

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=prefix,
    intents=intents,
    help_command=None
)




@bot.event
async def on_ready():
    os.system('cls')


    try:
        synced = await bot.tree.sync()
    except Exception as e:
        print(Colorate.Horizontal(Colors.light_red, "                                     [Error] loading slash commands."))

    menu_text = f"""     
                                     

                                         
                                              _____                  _              
                                             / ____|                | |             
                                            | (___  _ __   __ _ _ __| |_ __ _ _ __  
                                             \___ \| '_ \ / _` | '__| __/ _` | '_ \ 
                                             ____) | |_) | (_| | |  | || (_| | | | |
                                            |_____/| .__/ \__,_|_|   \__\__,_|_| |_|
                                                   | |                              
                                                   |_|                                                                  
                                        
                                     ╔══════════════════════════════════════════════════════╗
                                     ║                    Spartan V1                        ║
                                     ║                                                      ║
                                     ║          Successfully logged in as Spartan           ║
                                     ║          Loaded {len(bot.commands)} Commands!!       ║
                                     ║                                                      ║
                                     ╚══════════════════════════════════════════════════════╝ 
                        
"""
    print(Colorate.Horizontal(Colors.cyan_to_blue, menu_text))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

    print(Colorate.Horizontal(Colors.light_red, f"                                     [Error] Command error: {error}."))
    await ctx.send("⚠️ Something went wrong while running that command.")


async def load_cogs(): #cogs = command folder (/cogs by default)
    if not os.path.isdir("cogs"):
        print(Colorate.Horizontal(Colors.light_red, f"                                     [Error] Commands folder not found (/cogs)."))
        return

    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            extension = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(extension)
            except Exception as e:
                print(Colorate.Horizontal(Colors.light_red, f"                                     [Error] Failed to load {extension}: {e}."))

async def main():
    async with bot:
        await load_cogs()
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())