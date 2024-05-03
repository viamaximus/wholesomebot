import discord
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from collections import deque

class Infection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Dictionary to track member statuses (clean, exposed, or infected) and exposure scores.
        self.member_statuses = {}
        self.member_exposure_scores = {}

        # Queue to store recent interactions.
        self.recent_interactions = deque(maxlen=5)  # Store up to 5 interactions.

        # Initialize a scheduler.
        self.scheduler = AsyncIOScheduler()

        # Schedule the infect_highest_exposure task to run at 7 PM every day.
        self.scheduler.add_job(self.infect_highest_exposure, 'cron', hour=19)

        # Start the scheduler.
        self.scheduler.start()

    def set_member_status(self, member_id, status):
        """Set the status of a member."""
        self.member_statuses[member_id] = status
        self.member_exposure_scores[member_id] = 0  # Initialize exposure score to 0.

    def update_status_files(self):
        """Write member statuses to separate text files."""
        clean_members = []
        exposed_members = []
        infected_members = []

        for member_id, status in self.member_statuses.items():
            if status == 'clean':
                clean_members.append(str(member_id))
            elif status == 'exposed':
                exposed_members.append(str(member_id))
            elif status == 'infected':
                infected_members.append(str(member_id))

        # Write to text files.
        with open("clean_members.txt", "w") as clean_file:
            clean_file.write("\n".join(clean_members))

        with open("exposed_members.txt", "w") as exposed_file:
            exposed_file.write("\n".join(exposed_members))

        with open("infected_file.txt", "w") as infected_file:
            infected_file.write("\n".join(infected_members))

    @commands.Cog.listener()
    async def on_message(self, message):
        """Triggered when a new message is sent."""
        # Avoid responding to the bot's own messages.
        if message.author == self.bot.user:
            return

        author_id = message.author.id

        # Ensure the member's status and exposure score are initialized.
        if author_id not in self.member_statuses:
            self.set_member_status(author_id, 'clean')

        # Get the author's status.
        author_status = self.member_statuses[author_id]

        # Check message content for mentions to identify interactions.
        for mention in message.mentions:
            mention_id = mention.id

            # Ensure the mentioned member's status and exposure score are initialized.
            if mention_id not in self.member_statuses:
                self.set_member_status(mention_id, 'clean')

            mention_status = self.member_statuses[mention_id]

            # Add the interaction to the queue.
            self.recent_interactions.append((author_id, author_status, mention_id, mention_status))

        # Process recent interactions.
        for interaction in self.recent_interactions:
            author_id, author_status, mention_id, mention_status = interaction

            # Increment exposure scores based on interaction.
            if author_status == 'clean' and mention_status == 'infected':
                self.member_exposure_scores[author_id] += 1
            elif author_status == 'infected' and mention_status == 'clean':
                self.member_exposure_scores[mention_id] += 1

            # Check if exposure scores warrant a status change.
            exposure_threshold = 5  # Arbitrary threshold for demo purposes.
            if self.member_exposure_scores[author_id] >= exposure_threshold:
                self.member_statuses[author_id] = 'infected'
            if self.member_exposure_scores[mention_id] >= exposure_threshold:
                self.member_statuses[mention_id] = 'infected'

        await self.bot.process_commands(message)

    @commands.command()
    async def infect(self, ctx, member: discord.Member):
        """Manually infect a specific member."""
        self.member_statuses[member.id] = 'infected'
        await ctx.send(f"{member.name} is now infected!")

    async def infect_highest_exposure(self):
        """Infect the member with the highest exposure score."""
        # Get the member with the highest exposure score.
        max_exposure = max(self.member_exposure_scores.values(), default=0)
        most_exposed_members = [
            member_id for member_id, score in self.member_exposure_scores.items() if score == max_exposure
        ]

        if most_exposed_members:
            # Choose one member to infect.
            member_to_infect = most_exposed_members[0]

            # Set their status to infected.
            self.member_statuses[member_to_infect] = 'infected'

            # Log the infection event or handle it as needed.
            print(f"Member {member_to_infect} is now infected with an exposure score of {max_exposure}.")

            # Update the status files.
            self.update_status_files()
        else:
            print("No members found to infect.")

async def setup(client):
    await client.add_cog(Infection(client))