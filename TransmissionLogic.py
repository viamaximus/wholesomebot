import discord
import random

class TransmissionLogic:
    def __init__(self, bot):
        self.bot = bot

    async def infect_member(self, guild_id, top_members):
        chosen_member = self.weighted_choice(top_members)
        if chosen_member:
            await self.give_infected_role(guild_id, chosen_member)

    def weighted_choice(self, members):
        total = sum(2 ** i for i, _ in enumerate(reversed(members)))
        r = random.uniform(0, total)
        upto = 0
        for member_id, score in reversed(members):
            weight = 2 ** (len(members) - members.index((member_id, score)) - 1)
            if upto + weight > r:
                return member_id
            upto += weight

    async def give_infected_role(self, guild_id, member_id):
        guild = self.bot.get_guild(guild_id)
        role = discord.utils.get(guild.roles, name="InfectedRole")
        member = guild.get_member(member_id)
        if member and role:
            await member.add_roles(role)
            await member.send("Congratulations! You have been infected and now have access to special channels.")
            print(f"{member} has been infected.")
