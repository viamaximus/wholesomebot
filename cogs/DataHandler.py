import discord
from discord.ext import commands
import os
import json

class DataHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = 'userdata/members_data.json'
        self.data = self.load_data()
        print(f"DataHandler is ready. {len(self.data)} members loaded.")

    def load_data(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True) # Create the directory if it doesn't exist

        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.save_data({})
            return {}
        except json.JSONDecodeError:
            print(f"Error loading data ({e}). Initializing empty dataset.")
            self.save_data({})
            return {}

    def save_data(self, data=None):
        if data is not None:
            self.data = data
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)
            print(f"Data saved to {self.file_path}")

    async def get_data(self):
        print(f"Data requested. {len(self.data)} members loaded.")
        return self.data


    async def update_data(self, key, value):
        self.data[key] = value
        self.save_data()
        print(f"Data updated. {key}: {value}")

async def setup(bot):
    await bot.add_cog(DataHandler(bot))