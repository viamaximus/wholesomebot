import discord
from discord.ext import commands
import os
import json

class DataHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_file_path = 'userdata/members_data.json'
        self.guild_file_path = 'userdata/guild_data.json'
        self.userdata = self.load_user_data()
        self.guilddata = self.load_guild_data()
        print(f"DataHandler is ready. {len(self.userdata)} members loaded; {len(self.guilddata)} guilds loaded.")

    def load_user_data(self):
        os.makedirs(os.path.dirname(self.user_file_path), exist_ok=True) # Create the directory if it doesn't exist
        try:
            with open(self.user_file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.save_user_data({})
            return {}
        except json.JSONDecodeError as e:
            print(f"Error loading data ({e}). Initializing empty dataset.")
            self.save_user_data({})
            return {}
        
    def load_guild_data(self):
        os.makedirs(os.path.dirname(self.guild_file_path), exist_ok=True)
        try:
            with open(self.guild_file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.save_guild_data({})
            return {}
        except json.JSONDecodeError as e:
            print(f"Error loading data ({e}). Initializing empty dataset.")
            self.save_guild_data({})
            return {}

    def save_user_data(self, data=None):
        if data is not None:
            self.userdata = data
        with open(self.user_file_path, 'w') as f:
            json.dump(self.userdata, f, indent=4)
            #print(f"Data saved to {self.file_path}")

    def save_guild_data(self, data=None):
        if data is not None:
            self.guilddata = data
        with open(self.guild_file_path, 'w') as f:
            json.dump(self.guilddata, f, indent=4)
            #print(f"Data saved to {self.file_path}")

    async def get_user_data(self, guild_id=None):
        #print(f"Data requested. {len(self.data)} members loaded.")
        if guild_id:
            return self.userdata.get(guild_id, {})  # Return the guild data if it exists
        return self.userdata
    
    async def get_guild_data(self, guild_id=None):
        if guild_id:
            return self.guilddata.get(guild_id, {})
        return self.guilddata


    async def update_user_data(self, key, value):
        self.userdata[key] = value
        self.save_user_data()
        print(f"Data updated. {key}: {value}")

async def setup(bot):
    await bot.add_cog(DataHandler(bot))