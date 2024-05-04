from discord.ext import commands
import os
import json

class MemberLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.members_data = self.load_data()

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

    @commands.Cog.listener()
    async def on_ready(self):
        #log members when bot is ready
        for guild in self.bot.guilds:
            await self.log_members(guild)
        self.save_data()
        print('MemberLogger is ready')

    async def log_members(self, guild):
    #Logs each member in the guild to a JSON file.
        infected_role_name = "blueRole"
        members_data = {}
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

        # Ensure directory exists
        if not os.path.exists('userdata'):
            os.makedirs('userdata')

async def setup(bot):
    await bot.add_cog(MemberLogger(bot))