from typing import Final
import os
import asyncio
import discord
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands, tasks
from itertools import cycle

intents = discord.Intents.default()

client = commands.Bot(command_prefix='~', intents=intents.all())

#load token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

bot_status = cycle(['in my banky', ':3:3:#:3:3:3', 'mphghh...', 'in your walls', 'use "~" for commands!'])
@tasks.loop(seconds=10)                   
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

#handle startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')
    change_status.start()
    print(f'Logged in as {client.user}')

async def load():
    await client.load_extension('cogs.DataHandler') # Load the DataHandler cog first
    print(f"loaded DataHandler")
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != 'DataHandler.py':
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded {filename[:-3]}')

#main entry point
async def main():
    async with client: 
        await load()
        await client.start(TOKEN)

asyncio.run(main())