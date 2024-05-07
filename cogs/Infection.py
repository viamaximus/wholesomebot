import discord
from discord.ext import commands
import json
from datetime import datetime, timedelta
from DiceRoller import Dice
class Infection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_handler = self.bot.get_cog('DataHandler')
        self.keywords = self.load_keywords()

    def load_keywords(self):
        with open('userdata/.keywords', 'r') as file:
            return [line.strip() for line in file.readlines()]

    #triggered when a message is detected
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not self.data_handler:  # Ignore bots or if data handler isn't loaded
            return

        members_data = await self.data_handler.get_data()
        member_id = str(message.author.id)

        if member_id not in members_data:
            print(f"Member {message.author.name} not found in data")
            return

        # Detect keywords and handle infection status
        if any(keyword in message.content for keyword in self.keywords):
            members_data[member_id]['exposure_score'] += Dice.roll(1, 4)
            print(f"Detected keyword in message, incrementing score for {message.author.name} to {members_data[member_id]['exposure_score']}")

        if members_data[member_id]['exposure_status'] in ['exposed', 'infected']:
            members_data[member_id]['exposure_score'] += Dice.roll(2, 4)
            print(f"Incremented exposure score for {message.author.name} to {members_data[member_id]['exposure_score']}")
        else:
            members_data[member_id]['exposure_status'] = 'exposed'
            members_data[member_id]['exposure_score'] = Dice.roll(1, 8)
            print(f"Member {message.author.name} is now exposed; score set to {members_data[member_id]['exposure_score']}")

        # Save data once after all changes
        await self.data_handler.save_data(members_data)
        print("Data saved.")

    @commands.command() 
    async def status(self, ctx, member: discord.Member = None):
        member = member or ctx.author  # Default to the message author if no member is specified
        members_data = await self.data_handler.get_data()
        member_data = members_data.get(str(member.id))
        if member_data:
            await ctx.send(f"{member.name} is currently {member_data['exposure_status']}.")
        else:
            await ctx.send("Member data not found.")

async def setup(bot):
    await bot.add_cog(Infection(bot))