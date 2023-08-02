# 
# Tiramisu Discord Bot
# --------------------
# User Reports Commands
# 
from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from libs.database import Database
from typing import Optional

from libs import reports

class Reporting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog reporting.py')

    # Commands
    @nextcord.slash_command(description="Report a user or problem")
    async def report(self, interaction: nextcord.Interaction):
        pass

    @report.subcommand(description='Report a discord user to the moderators')
    async def user(self, interaction: nextcord.Interaction,
        user: Optional[nextcord.Member] = nextcord.SlashOption(description='Who to Report', required=True),
        reason: Optional[str] = nextcord.SlashOption(description='Why are you reporting this user?', required=True),):
        db = Database(interaction.guild, reason='Slash command `/report user`')
        try:
            modlog_channel =  interaction.guild.get_channel(int(db.fetch('modlog_channel')))
            if modlog_channel == None:
                raise ValueError
            else:
                await modlog_channel.send(f'**User Reported:**\nBy: {interaction.user.name}#{interaction.user.discriminator} (`{interaction.user.id}`)\
\nReported User: {user.mention} ({user.name}#{user.discriminator}`{user.id}`)\nReason: {reason}')
                logger.info('Successfully completed a warn action.')
                await interaction.send(f'Successfully sent your report to the moderators! Thanks for speaking up.', ephemeral=True)
        except ValueError:
            await interaction.send('The moderators have not yet (or incorrectly) set up where to send reports!\nAsk them to set the `modlog_channel` setting to the ID of the channel where logs should be sent.', ephemeral=True)
    
    @report.subcommand(description='Report a minecraft player to the moderators')
    async def player(self, interaction: nextcord.Interaction):
        await reports.player(interaction)

    @report.subcommand(description='Report a Bug')
    async def bug(self, interaction: nextcord.Interaction):
        await reports.bug(interaction)
def setup(bot):
    bot.add_cog(Reporting(bot))
    logger.debug('Setup cog "reporting"')