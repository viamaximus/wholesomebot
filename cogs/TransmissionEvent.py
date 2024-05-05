import discord
import random
import json
import os
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class TransmissionEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.file_path = 'userdata/scoreboard.txt'
        self.scheduler.add_job(self.sort_scoreboard, 'cron', hour=18, minute=45)  # Sort the scoreboard at 6:45 PM
        self.scheduler.add_job(self.infect_member, 'cron', hour=19)  # Infect a member at 7 PM
        self.scheduler.start()

    async def sort_scoreboard(self):
        # Load data, sort it, and save it back to the file
        members_data = self.load_scoreboard()
        sorted_members = sorted(members_data.items(), key=lambda x: x[1]['exposure_score'], reverse=True)
        with open(self.file_path, 'w') as f:
            for member_id, data in sorted_members:
                f.write(f"{member_id} {data['exposure_score']}\n")
        print("Scoreboard sorted.")    

    async def infect_member(self):
        # Choose and infect the member
        top_members = self.load_top_members(3)
        if top_members:
            chosen_member = self.weighted_choice(top_members)
            await self.give_infected_role(chosen_member)

    def load_scoreboard(self):
        with open(self.file_path, 'r') as f:
            return {line.split()[0]: {'exposure_score': int(line.split()[1])} for line in f if line.strip()}
        
    def load_top_members(self, count):
        with open(self.file_path, 'r') as f:
            lines = f.readlines()
        return [(line.split()[0], int(line.split()[1])) for line in lines[:count]]

    def weighted_choice(self, members):
        total = sum(2 ** i for i, _ in enumerate(reversed(members)))
        r = random.uniform(0, total)
        upto = 0
        for member_id, score in reversed(members):
            weight = 2 ** (len(members) - members.index((member_id, score)) - 1)
            if upto + weight >= r:
                return member_id
            upto += weight

    async def give_infected_role(self, member_id):
        #give the infected role to the member
        member = await self.bot.fetch_user(self, member_id)
        guild = self.bot.get_guild(self.guild_id)
        role = discord.utils.get(guild.roles, name="blueRole")
        await member.add_roles(role)
        await member.send("Congratulations! You have been infected. You now have acess to the infected channel. Alternatively, you can send $4.99 to max's venmo account to be cured.")
        print(f"{member.name} has been infected.")

async def setup(bot):
    await bot.add_cog(TransmissionEvent(bot))
    