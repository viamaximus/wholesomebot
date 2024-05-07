import discord
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from TransmissionLogic import TransmissionLogic
import random

class TaskScheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.transmission_logic = TransmissionLogic(bot)
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(self.trigger_infect_member, 'cron', hour=19)
        self.scheduler.start()


    async def trigger_infect_member(self):
        top_members = self.load_top_members(3)
        if top_members:
            chosen_member = self.weighted_choice(top_members)
            await self.give_infected_role(chosen_member)

        
    def weighted_choice(self, members):
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
        
    async def give_infected_role(self, member_id):
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

async def setup(bot):
    await bot.add_cog(TaskScheduler(bot))
