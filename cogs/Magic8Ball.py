import discord
from discord.ext import commands
from magicresponse import magic_responses
import random



class Magic8Ball(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #@commands.Cog.listener()
    #async def on_ready(self):
    #    print('Magic8Ball is ready')
    
    @commands.command(aliases=['8ball', 'eightball', '8 ball', 'eight ball'])
    async def magic8ball(self, ctx, *, question):
        if not magic_responses:
         response = "I don't have any responses right now."
        else:
            response = random.choice(magic_responses)
        await ctx.send(response)


async def setup(client):
    await client.add_cog(Magic8Ball(client))
