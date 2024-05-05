import discord
from discord.ext import commands
import json
import os

class CustomHelpCommand(commands.HelpCommand):
    def get_command_signature(self, command):
        return f'{self.clean_prefix}{command.qualified_name} {command.signature}'

    async def send_bot_help(self, mapping):
        channel = self.get_destination()
        help_text = "Here are all of my commands:\n\n"
        for cog, commands in mapping.items():
            filtered_commands = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(cmd) for cmd in filtered_commands]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                help_text += f"**{cog_name}**\n" + "\n".join(command_signatures) + "\n\n"
        await channel.send(help_text)

    async def send_command_help(self, command):
        channel = self.get_destination()
        help_text = f"**{command.name}**\n{command.help}\n\n"
        help_text += f"**Syntax:** {self.get_command_signature(command)}"
        await channel.send(help_text)

    async def send_group_help(self, group):
        channel = self.get_destination()
        help_text = f"**{group.name}**\n{group.help}\n\n"
        for cmd in group.commands:
            help_text += f"**{cmd.name}** - {cmd.help}\n"
        help_text += f"\nUse `{self.clean_prefix}help [command]` for more info on a command."
        await channel.send(help_text)

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = 'userdata/.config'
        self.scoreboard_file = 'userdata/scoreboard.txt'
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
    
    @commands.command(help = "Get the exposure score of a user.")
    async def score(self, ctx, username: discord.Member=None):
        username = username or ctx.author  # Default to the command sender if no user is specified
        data_handler = self.bot.get_cog('DataHandler')
        if not data_handler:
            await ctx.send("DataHandler cog is not loaded.")
            return
        data = await data_handler.get_data()  # Ensure this retrieves the data correctly
        user_data = data.get(str(username.id), {})  # Safely get the user data
        score = user_data.get('exposure_score', 0)  # Default to 0 if no score is found
        await ctx.send(f"{username.mention}'s exposure score is {score}.")

    @commands.command(help="Update and display the scoreboard.")
    #@commands.has_permissions(administrator=True)
    async def scoreboard(self, ctx):
        data_handler = self.bot.get_cog('DataHandler')
        if not data_handler:
            await ctx.send("DataHandler cog is not loaded.")
            return

        # Retrieve data and prepare scoreboard
        members_data = await data_handler.get_data()
        guild = ctx.guild
        scoreboard_content = []

        for member_id, info in members_data.items():
            member = guild.get_member(int(member_id))
            if member:
                username = member.display_name  # or member.name if you want the Discord username
                score = info.get('exposure_score', 0)
                scoreboard_content.append((username, score))
            else:
                print(f"Member with ID {member_id} not found in the guild.")

        # Sort the list of tuples by the score in descending order
        scoreboard_content.sort(key=lambda x: x[1], reverse=True)

        # Write the sorted data to the scoreboard file
        with open(self.scoreboard_file, 'w') as f:
            for username, score in scoreboard_content:
                f.write(f"{username} {score}\n")

        # Read and send the updated scoreboard
        with open(self.scoreboard_file, 'r') as f:
            scoreboard = f.read()
        await ctx.send(f"```{scoreboard}```")
        
    @commands.command(help = "Set the infected role.")
    async def configRole(self, ctx, role: discord.Role):
        self.config['infected_role'] = role.id
        self.save_config()
        await ctx.send(f"Infected role set to {role.name}.")

async def setup(bot):
    await bot.add_cog(UserCommands(bot))
