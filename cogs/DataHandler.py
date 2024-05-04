import discord
from discord.ext import commands
import os
import json

class DataHandler(commands.Cog):
    def __init__(self, bot):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(base_dir, 'userdata', 'members_data.json')
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

def setup(bot):
    bot.add_cog(DataHandler(bot))