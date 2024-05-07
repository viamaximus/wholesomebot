import discord
import random
import os
import json

class ScoreSystem:
    def score(self, ctx, username: discord.Member=None):
        username = username or ctx.author
        data_handler = self.bot.get_cog('DataHandler')
        if not data_handler:
            ctx.send("DataHandler cog is not loaded.")
            return
        data = data_handler.get_data()
        user_data = data.get(str(username.id), {})
