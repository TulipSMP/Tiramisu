import nextcord
from nextcord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    
    staff = 1035378549403684864
    TESTING_GUILD_ID=1035313572638638110

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog moderation.py loaded!')

    # Commands
    @commands.command(description="Warn a User", guild_ids=[TESTING_GUILD_ID])
    async def warn(interaction: nextcord.Interaction, arg: nextcord.Member, reason=str):
        if reason is None:
            reason = "No reason given."
        await arg.send(f"**You have been warned!**\nReason: __{reason}__\nPlease do not do this again. Make sure you have read the server rules.")
        await interaction.send(f"{arg.mention} has been warned for:\n{reason}")

def setup(bot):
    bot.add_cog(Moderation(bot))