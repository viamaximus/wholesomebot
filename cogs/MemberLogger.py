from discord.ext import commands
import os

class MemberLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        #log members when bot is ready
        for guild in self.bot.guilds:
            self.log_members(guild)

    def log_members(self, guild):
        #Logs each member in the guild to separate text files
        members_directory = f'userdata'
        if not os.path.exists(members_directory):
            os.makedirs(members_directory)

        for member in guild.members:
            with open(f'{members_directory}/{member.id}.txt', 'w') as file:
                file.write(f'ID: {member.id}\n')
                file.write(f'Name: {member.name}\n')
                file.write(f'Discriminator: {member.discriminator}\n')
                file.write(f'Joined at: {member.joined_at}\n')
                file.write(f'Bot: {member.bot}\n')

async def setup(bot):
    await bot.add_cog(MemberLogger(bot))