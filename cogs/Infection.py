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
        self.scheduler.add_job(self.update_infections, 'cron', hour=19)  # Infect one member daily at 7 PM
        self.scheduler.start()


    #triggered when a message from an infected member is detected
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not self.data_handler:
            print('Ignoring message, bot detected, or data not in handler')
            return
        
        members_data = self.data_handler.get_data()
        if str(message.author.id) not in members_data:
            return
        
        member_data = members_data[str(message.author.id)]
        if member_data['exposure_status'] == 'infected':
            await self.process_exposure(message)
    

    async def process_exposure(self, message, members_data):
        #Increments exposure scores based on interaction with an infected member.
        async for msg in message.channel.history(limit=5, after=message):   # Get the last 5 messages after the infected message
            if msg.author.id != message.author.id and msg.author.id in members_data: # If the message author is not the infected member and is in the data
                affected_member = members_data[str(msg.author.id)]
                if affected_member['exposure_status'] == 'clean':
                    affected_member['exposure_status'] = 'exposed'
                affected_member['exposure_score'] += 3
                print(f'Exposure score for was {msg.author.name}, is now {affected_member["exposure_score"]}.')
        await self.data_handler.save_data()

    def update_infections(self): 
        #Selects one member to infect based on the highest exposure score.
        highest_score = 0 # Initialize the highest score
        candidate = None # Initialize the candidate
        for member_id, data in self.members_data.items(): # Iterate over the members
            if data['exposure_status'] == 'exposed' and data['exposure_score'] > highest_score: # If the member is exposed and has a higher score
                highest_score = data['exposure_score'] # Update the highest score
                candidate = member_id # Update the candidate

        if candidate: # If a candidate was found
            self.members_data[candidate]['exposure_status'] = 'infected' # Set the exposure status to infected
            self.members_data[candidate]['infected_time'] = datetime.now().isoformat() # Set the infected time to the current time
            self.save_data() 
            print(f"Member {candidate} was infected on {datetime.now()}.") # Log the infection


    @commands.command() 
    async def status(self, ctx, member: discord.Member):
        member_data = self.members_data.get(str(member.id), None)
        if member_data:
            await ctx.send(f"{member.name} is currently {member_data['exposure_status']}.")
        else:
            await ctx.send("Member data not found.")

async def setup(bot):
    await bot.add_cog(Infection(bot))
