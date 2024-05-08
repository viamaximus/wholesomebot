import json
import discord
from discord.ext import commands
import aiofiles
import os

class Configurator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = {}
        self.data_handler = self.bot.get_cog('DataHandler')
        self.config_file_path = 'userdata/.config'
        self.keyword_file_path = 'userdata/.keywords'
        self.initialize_files()
        if not self.data_handler:
            print("DataHandler cog is not loaded.")
            return
        

    async def initialize_files(self):
        #initialize the config file if it doesnt exist
        if not os.path.exists(self.config_file_path):
           os.makedirs(os.path.dirname(self.config_file_path), exist_ok=True)
           await self.init_config()

        #initialize the keyword file if it doesnt exist
        if not os.path.exists(self.keyword_file_path):
            os.makedirs(os.path.dirname(self.keyword_file_path), exist_ok=True)
            self.init_keywords()

    async def init_config(self):
        self.config = {
            'infected_role_name': 'blueRole',
            'prefix': '~'
        }
        await self.save_config()
        
    async def save_config(self):
        async with aiofiles.open(self.config_file_path, 'w') as f:
            await f.write(json.dumps(self.config, indent=4))

    async def load_config(self):
        try:
            async with aiofiles.open(self.config_file_path, 'r') as f:
                self.config = await f.json()
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading config: {e}, reinitializing.")
            await self.init_config()
        
    async def get_config(self):
        if not self.config:
            await self.load_config()
        return self.config
    
    async def set_infected_role_name(self, role_name):
        self.config['infected_role_name'] = role_name
        await self.save_config()
    
    async def set_prefix(self, prefix):
        self.config['prefix'] = prefix
        await self.save_config()
    
    def get_prefix(self):
        return self.config['prefix']
    
    async def load_keywords(self):
        try:
            async with aiofiles.open(self.keyword_file_path, 'r') as file:
                return [line.strip() async for line in file]
        except FileNotFoundError:
            return []

    
async def setup(bot):
    await bot.add_cog(Configurator(bot))