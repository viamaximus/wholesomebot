from typing import Final
import os
import discord
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands, tasks
from responses import get_response
import random
from itertools import cycle

#load token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='~', intents=discord.Intents.all())

bot_status = cycle(['in my banky', ':3:3:#:3:3:3', 'mphghh...', 'in your walls'])
@tasks.loop(seconds=10)                   
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))


#handle startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')
    change_status.start()



@client.command(alias=['8ball', 'eightball', '8 ball', 'eight ball'])
async def magic8ball(ctx, *, question):
    with open('./8ballresponses.txt', 'r') as f:
        random_responses = f.readlines()
        response = random.choice(random_responses)
    await ctx.send(response)

@client.command()
async def ping(ctx):
    bot_latency = round(client.latency * 1000)
    await ctx.send(f"Bot latency: {bot_latency}ms")

#message functionality

async def send_message(message: Message, user_message: str) -> None:
    if not user_message: 
        print('(No message to send because intents were not enabled)')
        return
    #is_private = user_message[0] == '?'

    if is_private := user_message[0] == '?': 
        user_message = user_message[1:]
    try: 
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e: 
        print(e)

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


