import discord
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
#from TransmissionLogic import TransmissionLogic
import random
from UserCommands import UserCommands

class TaskScheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        #self.scheduler.add_job(self.trigger_infect_member(self), 'cron', hour=19)
        self.scheduler.add_job()
        self.scheduler.start()

    async def cue_infection(self, ctx):
        print("cuing infection")
        guild_id = ctx.guild.id
        await self.trigger_infect_member(guild_id)

    async def trigger_infect_member(self, guild_id):
        #Function to trigger infection based on the provided guild ID.
        print(f"Triggering infection in guild: {guild_id}")
        top_members = await self.load_top_members(guild_id, 3)
        if top_members:
            chosen_member = self.weighted_choice(top_members)
            await self.give_infected_role(guild_id, chosen_member)


        
    def weighted_choice(self, members):
        print("calculating weighted choice")
        try:
            total = sum(2 ** i for i, _ in enumerate(reversed(members)))
            r = random.uniform(0, total)
            upto = 0
            for member_id, score in reversed(members):
                weight = 2 ** (len(members) - members.index((member_id, score)) - 1)
                if upto + weight >= r:
                    return member_id
                upto += weight
        except Exception as e:
            print(f"Error in weighted choice: {e}")
            return None
        
    async def give_infected_role(self, member_id, guild_id):
        print("giving infected role")

        try:
            member = await self.bot.fetch_user(int(member_id))
            guild = self.bot.get_guild(self.guild_id)  # Ensure guild_id is correctly set somewhere accessible
            role = discord.utils.get(guild.roles, name="blueRole")
            if member and role:
                await member.add_roles(role)
                await member.send("Congratulations! You have been infected. You now have access to the infected channel.")
                print(f"{member} has been infected.")
        except Exception as e:
            print(f"Failed to give infected role: {e}")

    async def load_top_members(self, n):
        print("loading top members")
        try:
            data_handler = self.bot.get_cog('DataHandler')
            if not data_handler:
                print("DataHandler cog is not loaded.")
                return None
            members_data = await data_handler.get_data()
            return sorted(members_data.items(), key=lambda x: x[1]['exposure_score'], reverse=True)[:n]
        except Exception as e:
            print(f"Error loading top members: {e}")
            return None

async def setup(bot):
    await bot.add_cog(TaskScheduler(bot))
