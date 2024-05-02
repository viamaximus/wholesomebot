from typing import Final
import os
import asyncio
import discord
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands, tasks
from responses import get_response
from magicresponse import magic_responses

import random
from itertools import cycle

#load token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

#load prefix
client = commands.Bot(command_prefix='~', intents=discord.Intents.all())

bot_status = cycle(['in my banky', ':3:3:#:3:3:3', 'mphghh...', 'in your walls', 'use "~" for commands!'])
@tasks.loop(seconds=10)                   
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))


#handle startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded {filename[:-3]}')



#8ball game
@client.command(aliases=['8ball', 'eightball', '8 ball', 'eight ball'])
async def magic8ball(ctx, *, question):
    if not magic_responses:
        response = "I don't have any responses right now."
    else:
        response = random.choice(magic_responses)
    await ctx.send(response)


#main entry point
async def main():
    async with client: 
        await load()
        await client.start(TOKEN)

