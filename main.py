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

client = commands.Bot(command_prefix='~', intents=discord.Intents.all())

bot_status = cycle(['in my banky', ':3:3:#:3:3:3', 'mphghh...', 'in your walls', 'use "~" for commands!'])
@tasks.loop(seconds=10)                   
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))


#handle startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')
    change_status.start()


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded {filename[:-3]}')




#8ball game
@client.command(alias=['8ball', 'eightball', '8 ball', 'eight ball'])
async def magic8ball(ctx, *, question):
    if not magic_responses:
        response = "I don't have any responses right now."
    else:
        response = random.choice(magic_responses)
    await ctx.send(response)

#ping command
@client.command()
async def ping(ctx):
    bot_latency = round(client.latency * 1000)
    await ctx.send(f"Bot latency: {bot_latency}ms")

#handle incoming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user: 
        return
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'{username} said: {user_message} in {channel}')
    await send_message(message, user_message)

#main entry point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()


