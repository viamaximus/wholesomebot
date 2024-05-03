import discord
from discord.ext import commands, tasks
from collections import defaultdict, deque
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime

class Infection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.member_statuses = defaultdict(lambda: 'clean')  # Default to 'clean'
        self.exposure_scores = defaultdict(int)
        self.recent_messages = deque(maxlen=5)  # Track the last 5 messages for scoring

        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(self.update_infections, 'cron', hour=19)  # Run daily at 7 PM
        self.scheduler.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignore bot messages

        # Update recent messages
        self.recent_messages.append((message.author.id, message.channel.id))

        # Calculate exposure if the sender is infected
        if self.member_statuses[message.author.id] == 'infected':
            await self.calculate_exposure(message)
            self.write_statuses_to_files()

    async def calculate_exposure(self, message):
        # Check next five messages in the channel
        async for msg in message.channel.history(limit=5, after=message):
            if msg.author.id != message.author.id and self.member_statuses[msg.author.id] in ['clean', 'exposed']:
                self.exposure_scores[msg.author.id] += 3
                self.member_statuses[msg.author.id] = 'exposed'
                self.write_statuses_to_files()

    def update_infections(self):
        # Sort members by their exposure score in descending order
        exposed_members = {k: v for k, v in self.exposure_scores.items() if self.member_statuses[k] == 'exposed'}
        if exposed_members:
            highest_exposure_member = max(exposed_members, key=exposed_members.get)
            self.member_statuses[highest_exposure_member] = 'infected'
            print(f"Member {highest_exposure_member} has been infected on {datetime.datetime.now()}.")
            self.write_statuses_to_files()

    def write_statuses_to_files(self):
        with open("infection_data/clean_members.txt", "w") as clean_file, \
             open("infection_data/exposed_members.txt", "w") as exposed_file, \
             open("infection_data/infected_members.txt", "w") as infected_file:
            for member_id, status in self.member_statuses.items():
                if status == 'clean':
                    clean_file.write(f"{member_id}\n")
                elif status == 'exposed':
                    exposed_file.write(f"{member_id}\n")
                elif status == 'infected':
                    infected_file.write(f"{member_id}\n")

    @commands.command()
    async def status(self, ctx, member: discord.Member):
        #Check the status of a member.
        status = self.member_statuses[member.id]
        await ctx.send(f"{member.name} is currently {status}.")

async def setup(bot):
    await bot.add_cog(Infection(bot))
