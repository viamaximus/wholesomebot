import discord
from discord.ext import commands
import json
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class Infection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_handler = self.bot.get_cog('DataHandler')
        self.scheduler = AsyncIOScheduler()
        #self.scheduler.add_job(self.update_infections, 'cron', hour=19)  # Infect one member daily at 7 PM
        self.scheduler.start()


    #triggered when a message is detected
    @commands.Cog.listener()
    async def on_message(self, message):
        #print(f"Message from user {message.author} detected: {message.content}")
        if message.author.bot or not self.data_handler: # If the message author is a bot or the data handler is not available
            print('Ignoring message, bot detected, or data not in handler')
            return
        
        members_data = await self.data_handler.get_data()
        member_id = str(message.author.id)
        
        if member_id not in members_data: # If the message author is not in the data
            #print(f"Member {message.author.name} not found in data")
            return
        
        #print(f"message author passed checks")
        
        if members_data[member_id]['exposure_status'] in ['exposed', 'infected']:
            #print(f"Member {message.author.name} is exposed or infected.")
            members_data[member_id]['exposure_score'] += 1 # Increment the exposure score by 1
            print(f"incremented exposure score for {message.author.name} to {members_data[member_id]['exposure_score']}")
            await self.data_handler.save_data(members_data) # Save the data
            print(f"saved the data")
        else:
            print(f"Member {message.author.name} is clean.")
            #start tracking exposure if not already exposed or infected
            #this function is for testing only, turn off later.
            members_data[member_id]['exposure_status'] = 'exposed'
            members_data[member_id]['exposure_score'] = 1 # Set the exposure score to 1
            await self.data_handler.save_data(members_data) # Save the data
            print(f"Member {message.author.name} is now exposed.")

    @commands.command() 
    async def status(self, ctx, member: discord.Member = None):
        member = member or ctx.author  # Default to the message author if no member is specified
        members_data = await self.data_handler.get_data()
        member_data = members_data.get(str(member.id))
        if member_data:
            await ctx.send(f"{member.name} is currently {member_data['exposure_status']}.")
        else:
            await ctx.send("Member data not found.")

async def setup(bot):
    await bot.add_cog(Infection(bot))
