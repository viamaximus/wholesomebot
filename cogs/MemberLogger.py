import discord
from discord.ext import commands

class MemberLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_handler = self.bot.get_cog('DataHandler')

    @commands.Cog.listener()
    async def on_ready(self):
        #log members when bot is ready
        for guild in self.bot.guilds:
            await self.log_members(guild)
        await self.data_handler.save_data()
        print('MemberLogger is ready')

    async def log_members(self, guild):
    #Logs each member in the guild to a JSON file.
        infected_role_name = "blueRole"
        members_data = await self.data_handler.get_data()
        for member in guild.members:
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

        await self.data_handler.save_data()

async def setup(bot):
    await bot.add_cog(MemberLogger(bot))