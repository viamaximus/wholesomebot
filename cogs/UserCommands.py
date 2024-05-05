import discord
from discord.ext import commands
import json
import os

class UserCommands(commands.cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = 'userdata/.config'
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file):
            self.config = {}
            self.save_config()
        else:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    @commands.command()
    async def score(self, ctx, username: discord.Member=None):
        username = username or ctx.author
        data_handler = self.bot.get_cog('DataHandler')
        if not data_handler:
            await ctx.send("DataHandler cog is not loaded.")
            return
        data = await data_handler.get_data()
        user_data = data_handler.get_data(str(username.id))
        score = user_data.get('exposure_score', 0)
        await ctx.send(f"{username.mention}'s exposure score is {score}.")

    @commands.command()
    async def scoreboard(self, ctx):
        with open('userdata/scoreboard.txt', 'r') as f:
            scoreboard = f.readlines()
        await ctx.send(f"```{scoreboard}```")
    
    @commands.command()
    async def configRole(self, ctx, role: discord.Role):
        self.config['infected_role'] = role.id
        self.save_config()
        await ctx.send(f"Infected role set to {role.name}.")

    @commands.command()
    async def ping(self, ctx):
        ping_cog = self.bot.get_cog('Ping')
        if ping_cog: 
            await ping_cog.ping(ctx)
    
    @commands.command()
    async def ball(self, ctx, *, question):
        ball_cog = self.bot.get_cog('Magic8Ball')
        if ball_cog:
            await ball_cog.ball(ctx, question)

async def setup(bot):
    await bot.add_cog(UserCommands(bot))
