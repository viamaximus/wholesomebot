import discord
from discord.ext import commands
import json
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class Infection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.members_data = self.load_data()
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(self.update_infections, 'cron', hour=19)  # Infect one member daily at 7 PM
        self.scheduler.start()


    #SAVING AND LOADING DATA
    def load_data(self):
        #Loads member data from a JSON file.
        try:
            with open('userdata/members_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        
    def save_data(self):
            #Saves member data to a JSON file.
            with open('userdata/members_data.json', 'w') as f:
                json.dump(self.members_data, f, indent=4)


    #triggered when a message from an infected member is detected
    @commands.Cog.listener()
    async def on_message(self, message):
        print(f'Message detected from {message.author.name}.')
        print(f'procesing message {message.content}')
        if message.author.bot or message.author.id not in self.members_data: # Ignore bots and members not in the data
            print('Ignoring message, either bot or not in data')
            return

        member_data = self.members_data[str(message.author.id)] # Get the member's data
        if member_data['exposure_status'] == 'infected': # If the member is infected
            print(f'Infection detected in {message.author.name}.')
            await self.process_exposure(message) # Process the exposure

    async def process_exposure(self, message):
        #Increments exposure scores based on interaction with an infected member.
        async for msg in message.channel.history(limit=5, after=message):   # Get the last 5 messages after the infected message
            if msg.author.id != message.author.id and msg.author.id in self.members_data: # If the message author is not the infected member and is in the data
                affected_member = self.members_data[str(msg.author.id)] # Get the affected member's data
                if affected_member['exposure_status'] != 'infected': # If the affected member is not infected
                    print(f'no exposure detected in {msg.author.name}, continuing.')
                    if affected_member['exposure_status'] == 'clean':  # If the affected member is clean
                        print(f'user was clean, setting to exposed')
                        affected_member['exposure_status'] = 'exposed' # Set the exposure status to exposed
                    affected_member['exposure_score'] += 3 # Increment the exposure score by 3
                    print(f'Exposure score for was {msg.author.name}, is now {affected_member["exposure_score"]}.')
        self.save_data()

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
