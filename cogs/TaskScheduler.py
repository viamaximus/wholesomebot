import discord
from discord.ext import commands, tasks
import datetime
import random

transmissiontime = datetime.time(hour=20, minute=0, second=0)  # Set the time for the timed infection

class TaskScheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.infector_loop.start()
        
    @tasks.loop(seconds=10)
    async def infector_loop(self):
        print("Dummy task running.")
        #trigger the timed infection here
        for guild in self.bot.guilds:
            await self.trigger_infect_member(guild.id)

    async def trigger_infect_member(self, guild_id):
        # Function to trigger infection for all guilds
        print(f"Triggering infection in guild: {guild_id}")
        top_members = await self.load_top_exposed_members(guild_id, 3)
        if top_members:
            print(f"Top members: {top_members}")
            chosen_member = self.weighted_choice(top_members)
            print(f"Chosen member: {chosen_member}")
            await self.give_infected_role(chosen_member, guild_id)
        
        
    def weighted_choice(self, members):
        print("calculating weighted choice")
        try:
            # Members are passed as a list of (member_id, data) tuples
            total = sum(2 ** (len(members) - idx) for idx, (_, data) in enumerate(members))
            r = random.uniform(0, total)
            upto = 0
            for idx, (member_id, data) in enumerate(members):
                weight = 2 ** (len(members) - idx - 1)
                if upto + weight >= r:
                    return member_id
                upto += weight
        except Exception as e:
            print(f"Error in weighted choice: {e}")
            return None

        
    async def give_infected_role(self, member_id, guild_id):
        guild = self.bot.get_guild(guild_id)
        member = guild.get_member(member_id)
        role = discord.utils.get(guild.roles, name="blueRole")
        if member and role:
            await member.add_roles(role)
            print(f"Member {member.display_name} in guild {guild.name} has been infected.")


    async def load_top_members(self, n):
        print("loading top members")
        try:
            user_data_handler = self.bot.get_cog('DataHandler')
            if not user_data_handler:
                print("DataHandler cog is not loaded.")
                return None
            members_data = await user_data_handler.get_user_data()
            return sorted(members_data.items(), key=lambda x: x[1]['exposure_score'], reverse=True)[:n]
        except Exception as e:
            print(f"Error loading top members: {e}")
            return None
        
    async def load_top_exposed_members(self, guild_id, n):
        try:
            user_data_handler = self.bot.get_cog('DataHandler')
            if not user_data_handler:
                print("DataHandler cog is not loaded.")
                return []
            
            members_data = await user_data_handler.get_user_data(guild_id)
            if not members_data:
                print(f"No data returned for guild {guild_id}.")
                return []

            non_infected_members = {member_id: data for member_id, data in members_data.items() if data['exposure_status'] != 'infected'}
            sorted_members = sorted(non_infected_members.items(), key=lambda x: x[1]['exposure_score'], reverse=True)[:n]
            return sorted_members

        except Exception as e:
            print(f"Error loading top exposed members for guild {guild_id}: {e}")
            return []

async def setup(bot):
    
    await bot.add_cog(TaskScheduler(bot))
