import discord
from discord.ext import commands
import os

class MemberLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_handler = self.bot.get_cog('DataHandler')
        if not self.data_handler:
            print("DataHandler cog is not loaded.")
            return

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.data_handler:
            self.data_handler = self.bot.get_cog('DataHandler')
            if not self.data_handler:
                print("DataHandler still not loaded.")
                return
        
        #print("DataHandler is loaded, proceeding with member logging.")

        #print(f"logging members in {len(self.bot.guilds)} guilds")
        for guild in self.bot.guilds:
            #print(f"line25: Logging members for {guild.name}")
            await self.log_members(guild)
        
        if not self.data_handler:
            print("DataHandler cog is not loaded.")
            return
        print("datahandler is loaded")

        await self.data_handler.save_data()
        print('MemberLogger is ready')

    async def log_members(self, guild):
    #Logs each member in the guild to a JSON file.
        self.members_data = await self.data_handler.get_data()
        #print(f"line 39: starting Logging members in {guild.name}, with {len(guild.members)} members.")       

        infected_role_name = "blueRole"

        for member in guild.members:
            #print(f"Member {member.name} initializing")
            if str(member.id) not in self.members_data:
                is_infected=any(role.name == infected_role_name for role in member.roles)
                self.members_data[member.id] = {
                    'userid': str(member.id),
                    'username': member.name,
                    'discriminator': member.discriminator,
                    'bot': member.bot,
                    'exposure_status': 'infected' if is_infected else 'clean',  # Default status
                    'exposure_score': 0,  # Default score
                    'infected_time': None  # Default time
                }
                print(f"Member {member.name} logged, infected: {is_infected}, status: {self.members_data[member.id]['exposure_status']}, score: {self.members_data[member.id]['exposure_score']}, time: {self.members_data[member.id]['infected_time']}")

        await self.data_handler.save_data()
        #print(f"line 59: finished logging members in {guild.name}")

async def setup(bot):
    await bot.add_cog(MemberLogger(bot))